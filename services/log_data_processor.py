import logging
from datetime import datetime, timedelta
from sqlalchemy import func
from app import db
from models import LogReaderData, DailyLogSummary, WeeklyLogSummary, MonthlyLogSummary
from services.log_reader_service import LogReaderService

class LogDataProcessor:
    def __init__(self):
        self.log_reader = LogReaderService()
    
    def process_and_store_logs(self):
        """Process current logs and store in database"""
        try:
            logs = self.log_reader.get_log_reader_logs(lines=100)
            current_summary = self.log_reader.get_trading_summary()
            
            # Store the current status
            log_entry = LogReaderData(
                timestamp=datetime.utcnow(),
                log_type='status_snapshot',
                message='Periodic status snapshot',
                raw_data={
                    'logs_count': len(logs),
                    'summary': current_summary
                },
                buy_container_running=current_summary.get('buy_container_running', False),
                sell_container_running=current_summary.get('sell_container_running', False),
                api_calls_enabled=current_summary.get('api_enabled', False),
                live_trade_success_count=current_summary.get('live_trades_success', 0),
                live_trade_failure_count=current_summary.get('live_trades_failure', 0)
            )
            
            # Parse individual logs for detailed metrics
            for log in logs:
                if log.get('type') == 'status_update' and log.get('data'):
                    data = log['data']
                    key = list(data.keys())[0] if data else None
                    value = list(data.values())[0] if data else None
                    
                    if key == 'BUY Success Count':
                        try:
                            log_entry.buy_success_count = int(value)
                        except (ValueError, TypeError):
                            pass
                    elif key == 'BUY Stop Loss Count':
                        try:
                            log_entry.buy_stop_loss_count = int(value)
                        except (ValueError, TypeError):
                            pass
                    elif key == 'SELL Success Count':
                        try:
                            log_entry.sell_success_count = int(value)
                        except (ValueError, TypeError):
                            pass
                    elif key == 'SELL Stop Loss Count':
                        try:
                            log_entry.sell_stop_loss_count = int(value)
                        except (ValueError, TypeError):
                            pass
                    elif key == 'BUY Coins Tracking':
                        try:
                            log_entry.buy_coins_tracking = int(value)
                        except (ValueError, TypeError):
                            pass
                    elif key == 'SELL Coins Tracking':
                        try:
                            log_entry.sell_coins_tracking = int(value)
                        except (ValueError, TypeError):
                            pass
            
            db.session.add(log_entry)
            db.session.commit()
            
            logging.info(f"Stored log data entry at {log_entry.timestamp}")
            return True
            
        except Exception as e:
            logging.error(f"Error processing and storing logs: {e}")
            db.session.rollback()
            return False
    
    def generate_daily_summary(self, date=None):
        """Generate daily summary from log data"""
        if date is None:
            date = datetime.utcnow().date()
        
        try:
            # Get all log entries for the day
            start_date = datetime.combine(date, datetime.min.time())
            end_date = start_date + timedelta(days=1)
            
            daily_logs = LogReaderData.query.filter(
                LogReaderData.timestamp >= start_date,
                LogReaderData.timestamp < end_date
            ).all()
            
            if not daily_logs:
                return None
            
            # Calculate aggregates
            total_buy_success = max([log.buy_success_count for log in daily_logs], default=0)
            total_buy_failures = max([log.buy_stop_loss_count for log in daily_logs], default=0)
            total_sell_success = max([log.sell_success_count for log in daily_logs], default=0)
            total_sell_failures = max([log.sell_stop_loss_count for log in daily_logs], default=0)
            total_live_success = max([log.live_trade_success_count for log in daily_logs], default=0)
            total_live_failure = max([log.live_trade_failure_count for log in daily_logs], default=0)
            
            # Calculate averages
            avg_buy_coins = sum([log.buy_coins_tracking for log in daily_logs]) / len(daily_logs)
            avg_sell_coins = sum([log.sell_coins_tracking for log in daily_logs]) / len(daily_logs)
            
            # Calculate uptime percentages
            buy_running_count = sum([1 for log in daily_logs if log.buy_container_running])
            sell_running_count = sum([1 for log in daily_logs if log.sell_container_running])
            api_enabled_count = sum([1 for log in daily_logs if log.api_calls_enabled])
            
            buy_uptime = (buy_running_count / len(daily_logs)) * 24  # Hours
            sell_uptime = (sell_running_count / len(daily_logs)) * 24  # Hours
            api_duration = (api_enabled_count / len(daily_logs)) * 24  # Hours
            
            # Check if summary already exists
            existing = DailyLogSummary.query.filter_by(date=start_date).first()
            if existing:
                # Update existing
                existing.total_buy_success = total_buy_success
                existing.total_buy_failures = total_buy_failures
                existing.total_sell_success = total_sell_success
                existing.total_sell_failures = total_sell_failures
                existing.total_live_trades_success = total_live_success
                existing.total_live_trades_failure = total_live_failure
                existing.avg_buy_coins_tracking = avg_buy_coins
                existing.avg_sell_coins_tracking = avg_sell_coins
                existing.buy_container_uptime = buy_uptime
                existing.sell_container_uptime = sell_uptime
                existing.api_enabled_duration = api_duration
            else:
                # Create new
                summary = DailyLogSummary(
                    date=start_date,
                    total_buy_success=total_buy_success,
                    total_buy_failures=total_buy_failures,
                    total_sell_success=total_sell_success,
                    total_sell_failures=total_sell_failures,
                    total_live_trades_success=total_live_success,
                    total_live_trades_failure=total_live_failure,
                    avg_buy_coins_tracking=avg_buy_coins,
                    avg_sell_coins_tracking=avg_sell_coins,
                    buy_container_uptime=buy_uptime,
                    sell_container_uptime=sell_uptime,
                    api_enabled_duration=api_duration
                )
                db.session.add(summary)
            
            db.session.commit()
            logging.info(f"Generated daily summary for {date}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating daily summary: {e}")
            db.session.rollback()
            return False
    
    def generate_weekly_summary(self, week_start=None):
        """Generate weekly summary from daily summaries"""
        if week_start is None:
            today = datetime.utcnow().date()
            week_start = today - timedelta(days=today.weekday())
        
        try:
            week_end = week_start + timedelta(days=6)
            
            # Get daily summaries for the week
            daily_summaries = DailyLogSummary.query.filter(
                DailyLogSummary.date >= week_start,
                DailyLogSummary.date <= week_end
            ).all()
            
            if not daily_summaries:
                return False
            
            # Aggregate weekly data
            total_buy_success = sum([d.total_buy_success for d in daily_summaries])
            total_buy_failures = sum([d.total_buy_failures for d in daily_summaries])
            total_sell_success = sum([d.total_sell_success for d in daily_summaries])
            total_sell_failures = sum([d.total_sell_failures for d in daily_summaries])
            total_live_success = sum([d.total_live_trades_success for d in daily_summaries])
            total_live_failure = sum([d.total_live_trades_failure for d in daily_summaries])
            
            avg_buy_coins = sum([d.avg_buy_coins_tracking for d in daily_summaries]) / len(daily_summaries)
            avg_sell_coins = sum([d.avg_sell_coins_tracking for d in daily_summaries]) / len(daily_summaries)
            
            # Calculate success rate
            total_trades = total_buy_success + total_buy_failures + total_sell_success + total_sell_failures
            success_rate = ((total_buy_success + total_sell_success) / total_trades * 100) if total_trades > 0 else 0
            
            # Check if weekly summary exists
            existing = WeeklyLogSummary.query.filter_by(week_start=week_start).first()
            if existing:
                existing.total_buy_success = total_buy_success
                existing.total_buy_failures = total_buy_failures
                existing.total_sell_success = total_sell_success
                existing.total_sell_failures = total_sell_failures
                existing.total_live_trades_success = total_live_success
                existing.total_live_trades_failure = total_live_failure
                existing.avg_daily_buy_coins = avg_buy_coins
                existing.avg_daily_sell_coins = avg_sell_coins
                existing.success_rate = success_rate
            else:
                summary = WeeklyLogSummary(
                    week_start=week_start,
                    week_end=week_end,
                    total_buy_success=total_buy_success,
                    total_buy_failures=total_buy_failures,
                    total_sell_success=total_sell_success,
                    total_sell_failures=total_sell_failures,
                    total_live_trades_success=total_live_success,
                    total_live_trades_failure=total_live_failure,
                    avg_daily_buy_coins=avg_buy_coins,
                    avg_daily_sell_coins=avg_sell_coins,
                    success_rate=success_rate
                )
                db.session.add(summary)
            
            db.session.commit()
            logging.info(f"Generated weekly summary for week starting {week_start}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating weekly summary: {e}")
            db.session.rollback()
            return False
    
    def generate_monthly_summary(self, year=None, month=None):
        """Generate monthly summary from weekly summaries"""
        if year is None:
            year = datetime.utcnow().year
        if month is None:
            month = datetime.utcnow().month
        
        try:
            # Get weekly summaries for the month
            month_start = datetime(year, month, 1).date()
            if month == 12:
                month_end = datetime(year + 1, 1, 1).date() - timedelta(days=1)
            else:
                month_end = datetime(year, month + 1, 1).date() - timedelta(days=1)
            
            weekly_summaries = WeeklyLogSummary.query.filter(
                WeeklyLogSummary.week_start >= month_start,
                WeeklyLogSummary.week_start <= month_end
            ).all()
            
            if not weekly_summaries:
                return False
            
            # Aggregate monthly data
            total_buy_success = sum([w.total_buy_success for w in weekly_summaries])
            total_buy_failures = sum([w.total_buy_failures for w in weekly_summaries])
            total_sell_success = sum([w.total_sell_success for w in weekly_summaries])
            total_sell_failures = sum([w.total_sell_failures for w in weekly_summaries])
            total_live_success = sum([w.total_live_trades_success for w in weekly_summaries])
            total_live_failure = sum([w.total_live_trades_failure for w in weekly_summaries])
            
            avg_daily_volume = sum([w.avg_daily_buy_coins + w.avg_daily_sell_coins for w in weekly_summaries]) / len(weekly_summaries)
            avg_success_rate = sum([w.success_rate for w in weekly_summaries]) / len(weekly_summaries)
            
            # Check if monthly summary exists
            existing = MonthlyLogSummary.query.filter_by(year=year, month=month).first()
            if existing:
                existing.total_buy_success = total_buy_success
                existing.total_buy_failures = total_buy_failures
                existing.total_sell_success = total_sell_success
                existing.total_sell_failures = total_sell_failures
                existing.total_live_trades_success = total_live_success
                existing.total_live_trades_failure = total_live_failure
                existing.avg_daily_volume = avg_daily_volume
                existing.success_rate = avg_success_rate
            else:
                summary = MonthlyLogSummary(
                    year=year,
                    month=month,
                    total_buy_success=total_buy_success,
                    total_buy_failures=total_buy_failures,
                    total_sell_success=total_sell_success,
                    total_sell_failures=total_sell_failures,
                    total_live_trades_success=total_live_success,
                    total_live_trades_failure=total_live_failure,
                    avg_daily_volume=avg_daily_volume,
                    success_rate=avg_success_rate
                )
                db.session.add(summary)
            
            db.session.commit()
            logging.info(f"Generated monthly summary for {year}-{month}")
            return True
            
        except Exception as e:
            logging.error(f"Error generating monthly summary: {e}")
            db.session.rollback()
            return False
    
    def get_historical_data(self, period='daily', limit=30):
        """Get historical data for specified period"""
        try:
            if period == 'daily':
                data = DailyLogSummary.query.order_by(DailyLogSummary.date.desc()).limit(limit).all()
                return [{
                    'date': d.date.strftime('%Y-%m-%d'),
                    'buy_success': d.total_buy_success,
                    'buy_failures': d.total_buy_failures,
                    'sell_success': d.total_sell_success,
                    'sell_failures': d.total_sell_failures,
                    'live_success': d.total_live_trades_success,
                    'live_failure': d.total_live_trades_failure,
                    'success_rate': ((d.total_buy_success + d.total_sell_success) / 
                                   max(d.total_buy_success + d.total_buy_failures + d.total_sell_success + d.total_sell_failures, 1)) * 100
                } for d in reversed(data)]
                
            elif period == 'weekly':
                data = WeeklyLogSummary.query.order_by(WeeklyLogSummary.week_start.desc()).limit(limit).all()
                return [{
                    'date': d.week_start.strftime('%Y-%m-%d'),
                    'buy_success': d.total_buy_success,
                    'buy_failures': d.total_buy_failures,
                    'sell_success': d.total_sell_success,
                    'sell_failures': d.total_sell_failures,
                    'live_success': d.total_live_trades_success,
                    'live_failure': d.total_live_trades_failure,
                    'success_rate': d.success_rate
                } for d in reversed(data)]
                
            elif period == 'monthly':
                data = MonthlyLogSummary.query.order_by(MonthlyLogSummary.year.desc(), MonthlyLogSummary.month.desc()).limit(limit).all()
                return [{
                    'date': f"{d.year}-{d.month:02d}",
                    'buy_success': d.total_buy_success,
                    'buy_failures': d.total_buy_failures,
                    'sell_success': d.total_sell_success,
                    'sell_failures': d.total_sell_failures,
                    'live_success': d.total_live_trades_success,
                    'live_failure': d.total_live_trades_failure,
                    'success_rate': d.success_rate
                } for d in reversed(data)]
                
        except Exception as e:
            logging.error(f"Error getting historical data: {e}")
            return []
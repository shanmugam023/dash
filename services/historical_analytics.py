"""
Historical Analytics Service
Comprehensive trade history analysis with period-based comparisons
"""

import logging
from datetime import datetime, timedelta, date
from sqlalchemy import func, and_, or_
from app import db
from models import TradingSession, TradingStats

class HistoricalAnalytics:
    """Service for comprehensive historical trading analysis"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_period_comparison(self, period='today'):
        """
        Get Long vs Short comparison for specified period
        Periods: today, yesterday, week, month, year, all
        """
        end_date = datetime.utcnow().date()
        
        if period == 'today':
            start_date = end_date
        elif period == 'yesterday':
            start_date = end_date - timedelta(days=1)
            end_date = start_date
        elif period == 'week':
            start_date = end_date - timedelta(days=7)
        elif period == 'month':
            start_date = end_date - timedelta(days=30)
        elif period == 'year':
            start_date = end_date - timedelta(days=365)
        else:  # all time
            start_date = date(2020, 1, 1)  # Far back start date
            
        return self._get_period_stats(start_date, end_date)
    
    def _get_period_stats(self, start_date, end_date):
        """Get comprehensive stats for date range"""
        try:
            # Query for positions in date range
            query = TradingSession.query.filter(
                func.date(TradingSession.created_at) >= start_date,
                func.date(TradingSession.created_at) <= end_date
            )
            
            # Overall stats
            total_positions = query.count()
            
            # Long position stats
            long_query = query.filter(TradingSession.side == 'LONG')
            long_positions = long_query.count()
            long_profitable = long_query.filter(TradingSession.pnl > 0).count()
            long_total_pnl = long_query.with_entities(func.sum(TradingSession.pnl)).scalar() or 0
            
            # Short position stats
            short_query = query.filter(TradingSession.side == 'SHORT')
            short_positions = short_query.count()
            short_profitable = short_query.filter(TradingSession.pnl > 0).count()
            short_total_pnl = short_query.with_entities(func.sum(TradingSession.pnl)).scalar() or 0
            
            # Calculate success rates
            long_success_rate = (long_profitable / long_positions * 100) if long_positions > 0 else 0
            short_success_rate = (short_profitable / short_positions * 100) if short_positions > 0 else 0
            overall_success_rate = ((long_profitable + short_profitable) / total_positions * 100) if total_positions > 0 else 0
            
            return {
                'period': f"{start_date} to {end_date}",
                'total_positions': total_positions,
                'long': {
                    'positions': long_positions,
                    'profitable': long_profitable,
                    'success_rate': round(long_success_rate, 1),
                    'total_pnl': round(long_total_pnl, 2),
                    'avg_pnl': round(long_total_pnl / long_positions, 2) if long_positions > 0 else 0
                },
                'short': {
                    'positions': short_positions,
                    'profitable': short_profitable,
                    'success_rate': round(short_success_rate, 1),
                    'total_pnl': round(short_total_pnl, 2),
                    'avg_pnl': round(short_total_pnl / short_positions, 2) if short_positions > 0 else 0
                },
                'overall': {
                    'success_rate': round(overall_success_rate, 1),
                    'total_pnl': round(long_total_pnl + short_total_pnl, 2),
                    'best_side': 'LONG' if long_success_rate > short_success_rate else 'SHORT'
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating period stats: {e}")
            return self._empty_stats()
    
    def get_weekly_comparison(self, weeks_back=4):
        """Get Long vs Short comparison for last N weeks"""
        weekly_data = []
        today = datetime.utcnow().date()
        
        for i in range(weeks_back):
            week_end = today - timedelta(days=i*7)
            week_start = week_end - timedelta(days=6)
            
            stats = self._get_period_stats(week_start, week_end)
            stats['week_label'] = f"Week {i+1}"
            stats['week_start'] = week_start
            stats['week_end'] = week_end
            weekly_data.append(stats)
            
        return weekly_data
    
    def get_monthly_comparison(self, months_back=6):
        """Get Long vs Short comparison for last N months"""
        monthly_data = []
        today = datetime.utcnow().date()
        
        for i in range(months_back):
            # Calculate month boundaries
            if i == 0:
                month_end = today
                month_start = date(today.year, today.month, 1)
            else:
                temp_date = today.replace(day=1) - timedelta(days=i*30)
                month_start = date(temp_date.year, temp_date.month, 1)
                # Get last day of month
                if temp_date.month == 12:
                    month_end = date(temp_date.year + 1, 1, 1) - timedelta(days=1)
                else:
                    month_end = date(temp_date.year, temp_date.month + 1, 1) - timedelta(days=1)
            
            stats = self._get_period_stats(month_start, month_end)
            stats['month_label'] = month_start.strftime('%B %Y')
            stats['month_start'] = month_start
            stats['month_end'] = month_end
            monthly_data.append(stats)
            
        return monthly_data
    
    def get_performance_summary(self):
        """Get overall performance summary with key metrics"""
        try:
            # Get all-time stats
            all_time = self.get_period_comparison('all')
            
            # Get recent performance
            today_stats = self.get_period_comparison('today')
            week_stats = self.get_period_comparison('week')
            month_stats = self.get_period_comparison('month')
            
            # Best performing period
            periods = [
                ('Today', today_stats['overall']['success_rate']),
                ('This Week', week_stats['overall']['success_rate']),
                ('This Month', month_stats['overall']['success_rate']),
                ('All Time', all_time['overall']['success_rate'])
            ]
            
            best_period = max(periods, key=lambda x: x[1])
            
            return {
                'all_time': all_time,
                'recent': {
                    'today': today_stats,
                    'week': week_stats,
                    'month': month_stats
                },
                'best_period': {
                    'name': best_period[0],
                    'success_rate': best_period[1]
                },
                'recommendations': self._generate_recommendations(all_time, week_stats)
            }
            
        except Exception as e:
            self.logger.error(f"Error generating performance summary: {e}")
            return {}
    
    def _generate_recommendations(self, all_time, week_stats):
        """Generate trading recommendations based on historical data"""
        recommendations = []
        
        # Compare Long vs Short performance
        long_rate = all_time['long']['success_rate']
        short_rate = all_time['short']['success_rate']
        
        if long_rate > short_rate + 10:
            recommendations.append({
                'type': 'strategy',
                'message': f"Focus on LONG positions - {long_rate:.1f}% success rate vs {short_rate:.1f}% for SHORT"
            })
        elif short_rate > long_rate + 10:
            recommendations.append({
                'type': 'strategy', 
                'message': f"Focus on SHORT positions - {short_rate:.1f}% success rate vs {long_rate:.1f}% for LONG"
            })
        
        # Recent trend analysis
        week_long = week_stats['long']['success_rate']
        week_short = week_stats['short']['success_rate']
        
        if week_long > long_rate + 5:
            recommendations.append({
                'type': 'trend',
                'message': f"LONG positions trending up - {week_long:.1f}% this week vs {long_rate:.1f}% average"
            })
        
        if week_short > short_rate + 5:
            recommendations.append({
                'type': 'trend',
                'message': f"SHORT positions trending up - {week_short:.1f}% this week vs {short_rate:.1f}% average"
            })
        
        return recommendations
    
    def save_daily_stats(self, date_to_save=None):
        """Save or update daily statistics for historical tracking"""
        if date_to_save is None:
            date_to_save = datetime.utcnow().date()
            
        try:
            # Get stats for the day
            stats = self._get_period_stats(date_to_save, date_to_save)
            
            # Save stats for both users (combined for Long vs Short focus)
            for user in ['Yuva', 'Shan']:
                # Check if stats already exist
                existing = TradingStats.query.filter_by(
                    user=user,
                    period='daily',
                    period_date=datetime.combine(date_to_save, datetime.min.time())
                ).first()
                
                if existing:
                    # Update existing record
                    self._update_stats_record(existing, stats, user)
                else:
                    # Create new record
                    new_stats = TradingStats(
                        user=user,
                        period='daily',
                        period_date=datetime.combine(date_to_save, datetime.min.time())
                    )
                    self._update_stats_record(new_stats, stats, user)
                    db.session.add(new_stats)
            
            db.session.commit()
            self.logger.info(f"Daily stats saved for {date_to_save}")
            
        except Exception as e:
            self.logger.error(f"Error saving daily stats: {e}")
            db.session.rollback()
    
    def _update_stats_record(self, record, stats, user):
        """Update a TradingStats record with calculated stats"""
        # For simplicity, split stats between users
        user_multiplier = 0.6 if user == 'Yuva' else 0.4  # Yuva gets 60%, Shan gets 40%
        
        record.long_trades = int(stats['long']['positions'] * user_multiplier)
        record.long_successful = int(stats['long']['profitable'] * user_multiplier) 
        record.short_trades = int(stats['short']['positions'] * user_multiplier)
        record.short_successful = int(stats['short']['profitable'] * user_multiplier)
        record.total_trades = record.long_trades + record.short_trades
        record.successful_trades = record.long_successful + record.short_successful
        record.total_pnl = stats['overall']['total_pnl'] * user_multiplier
        record.win_rate = stats['overall']['success_rate']
        record.last_updated = datetime.utcnow()
    
    def _empty_stats(self):
        """Return empty stats structure"""
        return {
            'period': 'No data',
            'total_positions': 0,
            'long': {
                'positions': 0,
                'profitable': 0,
                'success_rate': 0,
                'total_pnl': 0,
                'avg_pnl': 0
            },
            'short': {
                'positions': 0,
                'profitable': 0,
                'success_rate': 0,
                'total_pnl': 0,
                'avg_pnl': 0
            },
            'overall': {
                'success_rate': 0,
                'total_pnl': 0,
                'best_side': 'LONG'
            }
        }

# Global instance
historical_analytics = HistoricalAnalytics()
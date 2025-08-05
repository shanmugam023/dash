import logging
from datetime import datetime, timedelta
from sqlalchemy import func
from app import db
from models import TradingSession, TradingStats

class TradingAnalytics:
    def __init__(self):
        pass

    def get_user_stats(self, user):
        """Get comprehensive trading statistics for a user"""
        try:
            # Get all trading sessions for user
            sessions = TradingSession.query.filter_by(user=user).all()
            
            stats = {
                'total_trades': len(sessions),
                'successful_trades': len([s for s in sessions if s.status == 'CLOSED' and s.pnl > 0]),
                'failed_trades': len([s for s in sessions if s.status == 'CLOSED' and s.pnl <= 0]),
                'long_trades': len([s for s in sessions if s.side == 'LONG']),
                'short_trades': len([s for s in sessions if s.side == 'SHORT']),
                'total_pnl': sum([s.pnl for s in sessions if s.pnl]),
                'open_positions': len([s for s in sessions if s.status == 'OPEN']),
                'win_rate': 0.0,
                'avg_profit': 0.0,
                'avg_loss': 0.0,
                'profit_factor': 0.0
            }
            
            # Calculate win rate
            closed_trades = [s for s in sessions if s.status == 'CLOSED']
            if closed_trades:
                winning_trades = [s for s in closed_trades if s.pnl > 0]
                stats['win_rate'] = (len(winning_trades) / len(closed_trades)) * 100
                
                # Calculate average profit/loss
                profits = [s.pnl for s in closed_trades if s.pnl > 0]
                losses = [abs(s.pnl) for s in closed_trades if s.pnl < 0]
                
                if profits:
                    stats['avg_profit'] = sum(profits) / len(profits)
                if losses:
                    stats['avg_loss'] = sum(losses) / len(losses)
                
                # Calculate profit factor
                total_profits = sum(profits) if profits else 0
                total_losses = sum(losses) if losses else 0
                if total_losses > 0:
                    stats['profit_factor'] = total_profits / total_losses
            
            return stats
            
        except Exception as e:
            logging.error(f"Error getting user stats for {user}: {e}")
            return {
                'total_trades': 0,
                'successful_trades': 0,
                'failed_trades': 0,
                'long_trades': 0,
                'short_trades': 0,
                'total_pnl': 0.0,
                'open_positions': 0,
                'win_rate': 0.0,
                'avg_profit': 0.0,
                'avg_loss': 0.0,
                'profit_factor': 0.0
            }

    def get_current_positions(self):
        """Get all current open positions"""
        try:
            positions = TradingSession.query.filter_by(status='OPEN').all()
            return [
                {
                    'user': pos.user,
                    'symbol': pos.symbol,
                    'side': pos.side,
                    'entry_price': pos.entry_price,
                    'position_size': pos.position_size,
                    'pnl': pos.pnl or 0.0,
                    'created_at': pos.created_at.strftime('%Y-%m-%d %H:%M:%S') if pos.created_at else 'N/A'
                }
                for pos in positions
            ]
        except Exception as e:
            logging.error(f"Error getting current positions: {e}")
            return []

    def update_statistics(self):
        """Update trading statistics in database"""
        try:
            for user in ['Yuva', 'Shan']:
                stats = self.get_user_stats(user)
                
                # Update or create stats record
                db_stats = TradingStats.query.filter_by(user=user).first()
                if db_stats:
                    db_stats.total_trades = stats['total_trades']
                    db_stats.successful_trades = stats['successful_trades']
                    db_stats.failed_trades = stats['failed_trades']
                    db_stats.long_trades = stats['long_trades']
                    db_stats.short_trades = stats['short_trades']
                    db_stats.total_pnl = stats['total_pnl']
                    db_stats.win_rate = stats['win_rate']
                    db_stats.last_updated = datetime.utcnow()
                else:
                    db_stats = TradingStats(
                        user=user,
                        total_trades=stats['total_trades'],
                        successful_trades=stats['successful_trades'],
                        failed_trades=stats['failed_trades'],
                        long_trades=stats['long_trades'],
                        short_trades=stats['short_trades'],
                        total_pnl=stats['total_pnl'],
                        win_rate=stats['win_rate']
                    )
                    db.session.add(db_stats)
            
            db.session.commit()
            
        except Exception as e:
            logging.error(f"Error updating statistics: {e}")
            db.session.rollback()

    def get_daily_pnl_chart_data(self, user, days=30):
        """Get daily PnL data for charts"""
        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            # Query closed positions within date range
            sessions = TradingSession.query.filter(
                TradingSession.user == user,
                TradingSession.status == 'CLOSED',
                TradingSession.closed_at >= start_date,
                TradingSession.closed_at <= end_date
            ).order_by(TradingSession.closed_at).all()
            
            # Group by date and sum PnL
            daily_pnl = {}
            for session in sessions:
                date_key = session.closed_at.strftime('%Y-%m-%d')
                if date_key not in daily_pnl:
                    daily_pnl[date_key] = 0
                daily_pnl[date_key] += session.pnl or 0
            
            # Fill missing dates with 0
            current_date = start_date
            chart_data = []
            while current_date <= end_date:
                date_key = current_date.strftime('%Y-%m-%d')
                chart_data.append({
                    'date': date_key,
                    'pnl': daily_pnl.get(date_key, 0)
                })
                current_date += timedelta(days=1)
            
            return chart_data
            
        except Exception as e:
            logging.error(f"Error getting daily PnL data: {e}")
            return []
    
    def get_trade_history_by_period(self, period):
        """Get trade history filtered by time period"""
        try:
            from datetime import datetime, timedelta
            
            now = datetime.utcnow()
            if period == 'today':
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif period == 'week':
                start_date = now - timedelta(days=7)
            elif period == 'month':
                start_date = now - timedelta(days=30)
            elif period == 'year':
                start_date = now - timedelta(days=365)
            else:  # 'all'
                start_date = datetime(2020, 1, 1)  # Far back date
            
            trades = TradingSession.query.filter(
                TradingSession.created_at >= start_date
            ).order_by(TradingSession.created_at.desc()).all()
            
            return [
                {
                    'id': trade.id,
                    'user': trade.user,
                    'symbol': trade.symbol,
                    'side': trade.side,
                    'entry_price': trade.entry_price,
                    'exit_price': trade.exit_price,
                    'position_size': trade.position_size,
                    'pnl': trade.pnl or 0.0,
                    'status': trade.status,
                    'created_at': trade.created_at.isoformat() if trade.created_at else None,
                    'closed_at': trade.closed_at.isoformat() if trade.closed_at else None
                }
                for trade in trades
            ]
            
        except Exception as e:
            logging.error(f"Error getting trade history by period: {e}")
            return []
    
    def get_user_stats_by_period(self, user, period):
        """Get user statistics for a specific time period"""
        try:
            from datetime import datetime, timedelta
            
            now = datetime.utcnow()
            if period == 'today':
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif period == 'week':
                start_date = now - timedelta(days=7)
            elif period == 'month':
                start_date = now - timedelta(days=30)
            elif period == 'year':
                start_date = now - timedelta(days=365)
            else:  # 'all'
                start_date = datetime(2020, 1, 1)
            
            sessions = TradingSession.query.filter(
                TradingSession.user == user,
                TradingSession.created_at >= start_date
            ).all()
            
            stats = {
                'total_trades': len(sessions),
                'successful_trades': len([s for s in sessions if s.status == 'CLOSED' and (s.pnl or 0) > 0]),
                'failed_trades': len([s for s in sessions if s.status == 'CLOSED' and (s.pnl or 0) <= 0]),
                'long_trades': len([s for s in sessions if s.side == 'LONG']),
                'short_trades': len([s for s in sessions if s.side == 'SHORT']),
                'long_successful': len([s for s in sessions if s.side == 'LONG' and s.status == 'CLOSED' and (s.pnl or 0) > 0]),
                'long_failed': len([s for s in sessions if s.side == 'LONG' and s.status == 'CLOSED' and (s.pnl or 0) <= 0]),
                'short_successful': len([s for s in sessions if s.side == 'SHORT' and s.status == 'CLOSED' and (s.pnl or 0) > 0]),
                'short_failed': len([s for s in sessions if s.side == 'SHORT' and s.status == 'CLOSED' and (s.pnl or 0) <= 0]),
                'total_pnl': sum([s.pnl or 0 for s in sessions]),
                'open_positions': len([s for s in sessions if s.status == 'OPEN']),
                'win_rate': 0.0,
                'avg_profit': 0.0,
                'avg_loss': 0.0,
                'profit_factor': 0.0,
                'period': period
            }
            
            # Calculate win rate and other metrics
            closed_trades = [s for s in sessions if s.status == 'CLOSED']
            if closed_trades:
                winning_trades = [s for s in closed_trades if (s.pnl or 0) > 0]
                stats['win_rate'] = (len(winning_trades) / len(closed_trades)) * 100
                
                profits = [s.pnl for s in closed_trades if (s.pnl or 0) > 0]
                losses = [abs(s.pnl) for s in closed_trades if (s.pnl or 0) < 0]
                
                if profits:
                    stats['avg_profit'] = sum(profits) / len(profits)
                if losses:
                    stats['avg_loss'] = sum(losses) / len(losses)
                
                total_profits = sum(profits) if profits else 0
                total_losses = sum(losses) if losses else 0
                if total_losses > 0:
                    stats['profit_factor'] = total_profits / total_losses
            
            return stats
            
        except Exception as e:
            logging.error(f"Error getting user stats by period: {e}")
            return {
                'total_trades': 0,
                'successful_trades': 0,
                'failed_trades': 0,
                'long_trades': 0,
                'short_trades': 0,
                'total_pnl': 0.0,
                'open_positions': 0,
                'win_rate': 0.0,
                'period': period
            }

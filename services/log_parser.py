import re
import logging
from datetime import datetime
from app import db
from models import TradingSession

class LogParser:
    def __init__(self):
        self.log_patterns = {
            'position_entry': r'📈 Managing (LONG|SHORT) position for ([A-Z]+USDT):',
            'position_size': r'Position Size: ([\d.]+)',
            'entry_price': r'Entry Price: ([\d.]+)',
            'current_price': r'Current Price: ([\d.]+)',
            'price_movement': r'Price Movement: ([\d.-]+)%',
            'success_count': r'(BUY|SELL) Success Count: (\d+)',
            'stop_loss_count': r'(BUY|SELL) Stop Loss Count: (\d+)',
            'live_trade_success': r'Live Trade Success Count: (\d+)',
            'live_trade_failure': r'Live Trade Failure Count: (\d+)',
            'container_status': r'(BUY|SELL) Container Running: (True|False)'
        }

    def parse_latest_logs(self):
        """Parse latest logs from containers"""
        try:
            # In a real implementation, you would read from the log files
            # For now, we'll simulate parsing the provided log data
            self._parse_sample_logs()
        except Exception as e:
            logging.error(f"Error parsing logs: {e}")

    def _parse_sample_logs(self):
        """Parse the sample log data provided"""
        sample_logs = [
            "📈 Managing LONG position for CHRUSDT:",
            "Position Size: 1755",
            "Entry Price: 0.0901",
            "Current Price: 0.0890",
            "📈 Managing LONG position for GHSTUSDT:",
            "Position Size: 365", 
            "Entry Price: 0.4330567123287",
            "Current Price: 0.4308000"
        ]
        
        try:
            current_symbol = None
            current_side = None
            current_data = {}
            
            for log_line in sample_logs:
                # Check for position entry
                position_match = re.search(self.log_patterns['position_entry'], log_line)
                if position_match:
                    if current_symbol and current_data:
                        self._save_position(current_symbol, current_side, current_data, 'Yuva')
                    
                    current_side = position_match.group(1)
                    current_symbol = position_match.group(2)
                    current_data = {}
                    continue
                
                # Parse position details
                size_match = re.search(self.log_patterns['position_size'], log_line)
                if size_match:
                    current_data['size'] = float(size_match.group(1))
                    continue
                
                entry_match = re.search(self.log_patterns['entry_price'], log_line)
                if entry_match:
                    current_data['entry_price'] = float(entry_match.group(1))
                    continue
                
                current_match = re.search(self.log_patterns['current_price'], log_line)
                if current_match:
                    current_data['current_price'] = float(current_match.group(1))
                    continue
            
            # Save the last position
            if current_symbol and current_data:
                self._save_position(current_symbol, current_side, current_data, 'Yuva')
                
        except Exception as e:
            logging.error(f"Error parsing sample logs: {e}")

    def _save_position(self, symbol, side, data, user):
        """Save position data to database"""
        try:
            # Check if position already exists
            existing_position = TradingSession.query.filter_by(
                user=user,
                symbol=symbol,
                status='OPEN'
            ).first()
            
            if existing_position:
                # Update existing position
                if 'current_price' in data:
                    existing_position.pnl = self._calculate_pnl(
                        existing_position.entry_price,
                        data['current_price'],
                        existing_position.position_size,
                        existing_position.side
                    )
                db.session.commit()
            else:
                # Create new position
                position = TradingSession(
                    user=user,
                    symbol=symbol,
                    side=side,
                    entry_price=data.get('entry_price', 0),
                    position_size=data.get('size', 0),
                    status='OPEN'
                )
                
                if 'current_price' in data:
                    position.pnl = self._calculate_pnl(
                        position.entry_price,
                        data['current_price'],
                        position.position_size,
                        position.side
                    )
                
                db.session.add(position)
                db.session.commit()
                
        except Exception as e:
            logging.error(f"Error saving position: {e}")
            db.session.rollback()

    def _calculate_pnl(self, entry_price, current_price, size, side):
        """Calculate PnL for a position"""
        try:
            if side == 'LONG':
                return (current_price - entry_price) * size
            else:  # SHORT
                return (entry_price - current_price) * size
        except:
            return 0.0

    def get_recent_logs(self, limit=50):
        """Get recent log entries"""
        # In a real implementation, this would read from actual log files
        # For now, return sample log data
        return [
            {
                'timestamp': '2025-08-05 07:19:05',
                'level': 'INFO',
                'message': '🔴 Containers detected running - DISABLING API calls',
                'source': 'strategy_manager'
            },
            {
                'timestamp': '2025-08-05 07:19:43',
                'level': 'INFO', 
                'message': 'Starting Trading Strategy Manager...',
                'source': 'strategy_manager'
            },
            {
                'timestamp': '2025-08-05 07:19:44',
                'level': 'INFO',
                'message': 'BUY Success Count: 0',
                'source': 'trading_bot'
            }
        ]

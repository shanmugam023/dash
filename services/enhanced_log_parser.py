import re
import logging
import os
from datetime import datetime
from app import db
from models import TradingSession

class EnhancedLogParser:
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
            'container_status': r'(BUY|SELL) Container Running: (True|False)',
            'new_position': r'🆕 New position detected - Original size: ([\d.]+)',
            'full_position': r'📊 Full position still active',
            'orders_set': r'✅ Orders already correctly set for ([A-Z]+USDT)',
            'checking_positions': r'🔄 Checking dynamic positions and orders',
            'fetching_positions': r'Fetching all open positions',
            'sleeping': r'⏰ Sleeping for (\d+) minute',
            'starting_bot': r'🚀 Starting Binance Futures Trading Bot',
            'strategy_info': r'📋 Strategy: (.+)',
        }
        
        # Container name to user mapping
        self.container_user_map = {
            'Yuva_Positions_trading_bot': 'Yuva',
            'Shan_Positions_trading_bot': 'Shan'
        }

    def parse_container_logs(self, container_name):
        """Parse logs from a specific container"""
        try:
            import docker
            client = docker.from_env()
            container = client.containers.get(container_name)
            
            # Get last 100 lines of logs
            logs = container.logs(tail=100, timestamps=True).decode('utf-8')
            
            user = self.container_user_map.get(container_name, 'Unknown')
            self._parse_log_content(logs, user)
            
        except Exception as e:
            logging.error(f"Error parsing container logs for {container_name}: {e}")

    def parse_latest_logs(self):
        """Parse latest logs from all containers"""
        try:
            # Parse logs from both trading containers
            for container_name in self.container_user_map.keys():
                self.parse_container_logs(container_name)
                
            # Also parse sample data for demonstration
            self._parse_sample_logs()
            
        except Exception as e:
            logging.error(f"Error parsing latest logs: {e}")

    def _parse_log_content(self, log_content, user):
        """Parse log content and extract trading information"""
        lines = log_content.split('\n')
        
        current_symbol = None
        current_side = None
        current_data = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Extract timestamp if present
            timestamp_match = re.match(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z)', line)
            if timestamp_match:
                line = line[len(timestamp_match.group(1)):].strip()
            
            # Check for position entry
            position_match = re.search(self.log_patterns['position_entry'], line)
            if position_match:
                # Save previous position if exists
                if current_symbol and current_data:
                    self._save_position(current_symbol, current_side, current_data, user)
                
                current_side = position_match.group(1)
                current_symbol = position_match.group(2)
                current_data = {'timestamp': datetime.utcnow()}
                continue
            
            # Parse position details
            if current_symbol:
                size_match = re.search(self.log_patterns['position_size'], line)
                if size_match:
                    current_data['size'] = float(size_match.group(1))
                    continue
                
                entry_match = re.search(self.log_patterns['entry_price'], line)
                if entry_match:
                    current_data['entry_price'] = float(entry_match.group(1))
                    continue
                
                current_match = re.search(self.log_patterns['current_price'], line)
                if current_match:
                    current_data['current_price'] = float(current_match.group(1))
                    continue
                
                movement_match = re.search(self.log_patterns['price_movement'], line)
                if movement_match:
                    current_data['price_movement'] = float(movement_match.group(1))
                    continue
                
                # Check for new position marker
                if re.search(self.log_patterns['new_position'], line):
                    current_data['is_new'] = True
                    continue
        
        # Save the last position
        if current_symbol and current_data:
            self._save_position(current_symbol, current_side, current_data, user)

    def _parse_sample_logs(self):
        """Parse sample log data for demonstration"""
        sample_logs = [
            "📈 Managing LONG position for AVAUSDT:",
            "Position Size: 268.5",
            "Entry Price: 0.5615128119181",
            "Current Price: 0.5573000",
            "🆕 New position detected - Original size: 268.5",
            "Price Movement: 0.75%",
            "📈 Managing LONG position for CHRUSDT:",
            "Position Size: 1755",
            "Entry Price: 0.0901",
            "Current Price: 0.0890",
            "Price Movement: 1.22%",
            "📈 Managing LONG position for GHSTUSDT:",
            "Position Size: 365", 
            "Entry Price: 0.4330567123287",
            "Current Price: 0.4308000",
            "Price Movement: 0.52%"
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
                        # Alternate between Yuva and Shan for demo
                        user = 'Yuva' if current_symbol in ['AVAUSDT', 'GHSTUSDT'] else 'Shan'
                        self._save_position(current_symbol, current_side, current_data, user)
                    
                    current_side = position_match.group(1)
                    current_symbol = position_match.group(2)
                    current_data = {'timestamp': datetime.utcnow()}
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
                
                movement_match = re.search(self.log_patterns['price_movement'], log_line)
                if movement_match:
                    current_data['price_movement'] = float(movement_match.group(1))
                    continue
                
                # Check for new position marker
                if re.search(self.log_patterns['new_position'], log_line):
                    current_data['is_new'] = True
                    continue
            
            # Save the last position
            if current_symbol and current_data:
                user = 'Yuva' if current_symbol in ['AVAUSDT', 'GHSTUSDT'] else 'Shan'
                self._save_position(current_symbol, current_side, current_data, user)
                
        except Exception as e:
            logging.error(f"Error parsing sample logs: {e}")

    def _save_position(self, symbol, side, data, user):
        """Save or update position data in database"""
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
                    existing_position.unrealized_pnl = self._calculate_pnl(
                        existing_position.entry_price,
                        data['current_price'],
                        existing_position.position_size,
                        existing_position.side
                    )
                    existing_position.pnl = existing_position.unrealized_pnl
                
                # Update price movement data
                if 'price_movement' in data:
                    existing_position.notes = f"Price Movement: {data['price_movement']}%"
                
                db.session.commit()
                logging.info(f"Updated position for {user}: {symbol} {side}")
                
            else:
                # Create new position
                position = TradingSession(
                    user=user,
                    symbol=symbol,
                    side=side,
                    entry_price=data.get('entry_price', 0),
                    position_size=data.get('size', 0),
                    status='OPEN',
                    trade_type='AUTO',
                    strategy='Binance Futures Bot',
                    created_at=data.get('timestamp', datetime.utcnow())
                )
                
                # Calculate unrealized PnL if current price available
                if 'current_price' in data:
                    position.unrealized_pnl = self._calculate_pnl(
                        position.entry_price,
                        data['current_price'],
                        position.position_size,
                        position.side
                    )
                    position.pnl = position.unrealized_pnl
                
                # Add price movement note
                if 'price_movement' in data:
                    position.notes = f"Price Movement: {data['price_movement']}%"
                
                db.session.add(position)
                db.session.commit()
                logging.info(f"Created new position for {user}: {symbol} {side} at {position.entry_price}")
                
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

    def close_position(self, user, symbol, exit_price):
        """Close a position and calculate realized PnL"""
        try:
            position = TradingSession.query.filter_by(
                user=user,
                symbol=symbol,
                status='OPEN'
            ).first()
            
            if position:
                position.exit_price = exit_price
                position.closed_at = datetime.utcnow()
                position.status = 'CLOSED'
                position.realized_pnl = self._calculate_pnl(
                    position.entry_price,
                    exit_price,
                    position.position_size,
                    position.side
                )
                position.pnl = position.realized_pnl
                
                db.session.commit()
                logging.info(f"Closed position for {user}: {symbol} with PnL: {position.realized_pnl}")
                return True
                
        except Exception as e:
            logging.error(f"Error closing position: {e}")
            db.session.rollback()
        
        return False

    def get_recent_logs(self, limit=50):
        """Get recent log entries formatted for display"""
        try:
            # Get recent trading sessions for log display
            sessions = TradingSession.query.order_by(
                TradingSession.created_at.desc()
            ).limit(limit).all()
            
            logs = []
            for session in sessions:
                log_entry = {
                    'timestamp': session.created_at.strftime('%Y-%m-%d %H:%M:%S') if session.created_at else 'N/A',
                    'level': 'INFO',
                    'message': f"{session.side} position for {session.symbol}: Entry=${session.entry_price:.4f}, Size={session.position_size}, PnL=${session.pnl:.2f}",
                    'source': f"{session.user.lower()}_trading_bot",
                    'user': session.user,
                    'symbol': session.symbol,
                    'status': session.status
                }
                logs.append(log_entry)
            
            return logs
            
        except Exception as e:
            logging.error(f"Error getting recent logs: {e}")
            return []
import random
import logging
import threading
import time
from datetime import datetime, timedelta
from app import db
from models import TradingSession

class LiveTradingSimulator:
    def __init__(self):
        self.symbols = ['AVAUSDT', 'STEEMUSDT', 'CHRUSDT', 'GHSTUSDT', 'BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOTUSDT']
        self.users = ['Yuva', 'Shan']
        self.running = False
        self.positions = {
            'Yuva': [],
            'Shan': []
        }
        
    def initialize_current_positions(self):
        """Initialize with some active positions - call from app context"""
        try:
            from app import app
            with app.app_context():
                # Clear existing positions first
                existing_sessions = TradingSession.query.filter_by(status='OPEN').all()
                
                # Initialize some sample positions if none exist
                if not existing_sessions:
                    self._create_sample_position('Yuva', 'AVAUSDT', 'LONG', 0.5615, 268.50)
                    self._create_sample_position('Yuva', 'STEEMUSDT', 'LONG', 0.1343, 1327.00)
                    self._create_sample_position('Shan', 'CHRUSDT', 'LONG', 0.0901, 1755.00)
                    self._create_sample_position('Shan', 'GHSTUSDT', 'LONG', 0.4331, 365.00)
                    
                    db.session.commit()
                    logging.info("Initialized sample trading positions")
                    
        except Exception as e:
            logging.error(f"Error initializing positions: {e}")
            
    def _create_sample_position(self, user, symbol, side, entry_price, size):
        """Create a sample position"""
        session = TradingSession(
            user=user,
            symbol=symbol,
            side=side,
            entry_price=entry_price,
            size=size,
            entry_time=datetime.utcnow(),
            status='OPEN'
        )
        db.session.add(session)
        
    def get_live_positions(self):
        """Get current live positions"""
        try:
            positions = TradingSession.query.filter_by(status='OPEN').all()
            live_data = []
            
            for pos in positions:
                # Simulate live price movement
                current_price = self._simulate_price_movement(pos.entry_price)
                pnl = self._calculate_pnl(pos.entry_price, current_price, pos.size, pos.side)
                
                live_data.append({
                    'symbol': pos.symbol,
                    'user': pos.user,
                    'side': pos.side,
                    'entry_price': pos.entry_price,
                    'current_price': current_price,
                    'size': pos.size,
                    'pnl': pnl,
                    'status': 'OPEN',
                    'time': pos.entry_time.strftime('%Y-%m-%d %H:%M:%S')
                })
                
            return live_data
            
        except Exception as e:
            logging.error(f"Error getting live positions: {e}")
            return []
            
    def _simulate_price_movement(self, entry_price):
        """Simulate realistic price movement"""
        # Random price movement between -5% to +5%
        movement_percent = random.uniform(-0.05, 0.05)
        current_price = entry_price * (1 + movement_percent)
        return round(current_price, 4)
        
    def _calculate_pnl(self, entry_price, current_price, size, side):
        """Calculate P&L for a position"""
        if side == 'LONG':
            pnl = (current_price - entry_price) * size
        else:  # SHORT
            pnl = (entry_price - current_price) * size
        return round(pnl, 2)
        
    def simulate_new_trade(self):
        """Simulate a new trade being opened"""
        try:
            user = random.choice(self.users)
            symbol = random.choice(self.symbols)
            side = random.choice(['LONG', 'SHORT'])
            entry_price = random.uniform(0.1, 2.0)
            size = random.uniform(100, 2000)
            
            # Create new trading session
            session = TradingSession(
                user=user,
                symbol=symbol,
                side=side,
                entry_price=entry_price,
                size=size,
                entry_time=datetime.utcnow(),
                status='OPEN'
            )
            
            db.session.add(session)
            db.session.commit()
            
            logging.info(f"Simulated new {side} position for {user}: {symbol} at {entry_price}")
            return session
            
        except Exception as e:
            logging.error(f"Error simulating new trade: {e}")
            return None
            
    def close_random_position(self):
        """Close a random open position"""
        try:
            open_positions = TradingSession.query.filter_by(status='OPEN').all()
            
            if open_positions:
                position = random.choice(open_positions)
                current_price = self._simulate_price_movement(position.entry_price)
                pnl = self._calculate_pnl(position.entry_price, current_price, position.size, position.side)
                
                position.exit_price = current_price
                position.exit_time = datetime.utcnow()
                position.pnl = pnl
                position.status = 'CLOSED'
                
                db.session.commit()
                
                logging.info(f"Closed {position.side} position for {position.user}: {position.symbol} with P&L: {pnl}")
                return position
                
        except Exception as e:
            logging.error(f"Error closing random position: {e}")
            return None
            
    def get_trading_stats(self, user=None, period='today'):
        """Get trading statistics for analysis"""
        try:
            # Calculate date range based on period
            now = datetime.utcnow()
            if period == 'today':
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif period == 'week':
                start_date = now - timedelta(days=7)
            elif period == 'month':
                start_date = now - timedelta(days=30)
            else:  # all time
                start_date = datetime(2020, 1, 1)
                
            query = TradingSession.query.filter(TradingSession.entry_time >= start_date)
            
            if user:
                query = query.filter_by(user=user)
                
            sessions = query.all()
            
            stats = {
                'total_trades': len(sessions),
                'long_trades': len([s for s in sessions if s.side == 'LONG']),
                'short_trades': len([s for s in sessions if s.side == 'SHORT']),
                'open_positions': len([s for s in sessions if s.status == 'OPEN']),
                'closed_trades': len([s for s in sessions if s.status == 'CLOSED']),
                'total_pnl': sum([s.pnl or 0 for s in sessions if s.pnl]),
                'winning_trades': len([s for s in sessions if s.pnl and s.pnl > 0]),
                'losing_trades': len([s for s in sessions if s.pnl and s.pnl < 0])
            }
            
            return stats
            
        except Exception as e:
            logging.error(f"Error getting trading stats: {e}")
            return {}

# Global simulator instance
live_simulator = LiveTradingSimulator()
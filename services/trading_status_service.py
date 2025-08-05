import logging
from datetime import datetime
import os

class TradingStatusService:
    """Service to parse and provide real trading status from logs"""
    
    def __init__(self):
        self.current_status = {}
        self.last_updated = None
        
    def parse_status_from_logs(self, log_content=None):
        """Parse trading status from log content"""
        # Default status structure
        status = {
            'buy_coins_tracking': [],
            'sell_coins_tracking': [],
            'buy_success_count': 0,
            'buy_stop_loss_count': 0,
            'sell_success_count': 0,
            'sell_stop_loss_count': 0,
            'live_trade_success_count': 0,
            'live_trade_failure_count': 0,
            'buy_container_running': False,
            'sell_container_running': False,
            'waiting_for_buy_start': False,
            'waiting_for_sell_start': False,
            'api_calls_enabled': False,
            'weekly_reset_in_progress': False,
            'current_time': '',
            'next_weekly_reset': '',
            'mode': 'Demo'  # Demo or Live
        }
        
        # If no log content provided, use demo data
        if not log_content:
            # Demo mode with sample data
            status.update({
                'buy_coins_tracking': [
                    {'symbol': 'AVAUSDT', 'entry': 0.5615, 'added': '2025-08-05 16:07:50'},
                    {'symbol': 'STEEMUSDT', 'entry': 0.1343, 'added': '2025-08-05 16:08:15'}
                ],
                'sell_coins_tracking': [
                    {'symbol': 'ZECUSDT', 'entry': 36.19, 'added': '2025-08-05 16:13:59'}
                ],
                'buy_success_count': 2,
                'buy_stop_loss_count': 1,
                'sell_success_count': 1,
                'sell_stop_loss_count': 0,
                'api_calls_enabled': True,
                'current_time': datetime.now().strftime('%A %Y-%m-%d %H:%M:%S'),
                'next_weekly_reset': 'Monday 2025-08-11 05:30:00 IST',
                'mode': 'Demo'
            })
            
            self.current_status = status
            self.last_updated = datetime.now()
            return status
        
        try:
            # Parse log content (simulate real log parsing)
            lines = log_content.split('\n')
            
            for line in lines:
                if 'BUY Coins Tracking:' in line:
                    count = int(line.split(':')[1].strip())
                    status['buy_coins_tracking'] = []
                    
                elif 'SELL Coins Tracking:' in line:
                    count = int(line.split(':')[1].strip())
                    status['sell_coins_tracking'] = []
                    
                elif 'BUY Success Count:' in line:
                    status['buy_success_count'] = int(line.split(':')[1].strip())
                    
                elif 'BUY Stop Loss Count:' in line:
                    status['buy_stop_loss_count'] = int(line.split(':')[1].strip())
                    
                elif 'SELL Success Count:' in line:
                    status['sell_success_count'] = int(line.split(':')[1].strip())
                    
                elif 'SELL Stop Loss Count:' in line:
                    status['sell_stop_loss_count'] = int(line.split(':')[1].strip())
                    
                elif 'Live Trade Success Count:' in line:
                    status['live_trade_success_count'] = int(line.split(':')[1].strip())
                    
                elif 'Live Trade Failure Count:' in line:
                    status['live_trade_failure_count'] = int(line.split(':')[1].strip())
                    
                elif 'BUY Container Running:' in line:
                    status['buy_container_running'] = 'True' in line
                    
                elif 'SELL Container Running:' in line:
                    status['sell_container_running'] = 'True' in line
                    
                elif 'API Calls Enabled:' in line:
                    status['api_calls_enabled'] = 'True' in line
                    
                elif 'Weekly Reset In Progress:' in line:
                    status['weekly_reset_in_progress'] = 'True' in line
                    
                elif 'Current IST Time:' in line:
                    status['current_time'] = line.split(':', 1)[1].strip()
                    
                elif 'Next Weekly Reset:' in line:
                    status['next_weekly_reset'] = line.split(':', 1)[1].strip()
                    
                # Parse coin entries
                elif line.strip().startswith('-') and 'Entry' in line:
                    # Parse coin tracking lines like:
                    # -   BABYUSDT: Entry 0.06034 (Added: 2025-08-05 16:07:50)
                    parts = line.strip()[1:].strip().split(':')
                    if len(parts) >= 2:
                        symbol = parts[0].strip()
                        entry_part = parts[1].strip()
                        
                        # Extract entry price
                        entry_price = 0.0
                        added_time = ''
                        
                        if 'Entry' in entry_part:
                            try:
                                price_str = entry_part.split('Entry')[1].split('(')[0].strip()
                                entry_price = float(price_str)
                                
                                if 'Added:' in entry_part:
                                    added_time = entry_part.split('Added:')[1].strip(' )')
                                    
                            except ValueError:
                                pass
                                
                        coin_data = {
                            'symbol': symbol,
                            'entry': entry_price,
                            'added': added_time
                        }
                        
                        # Add to appropriate list based on previous context
                        # This is simplified - in real implementation, track context better
                        if len(status['buy_coins_tracking']) < 10:  # Assume first coins are BUY
                            status['buy_coins_tracking'].append(coin_data)
                        else:
                            status['sell_coins_tracking'].append(coin_data)
            
            # Determine mode based on container status
            if status['buy_container_running'] or status['sell_container_running']:
                status['mode'] = 'Live'
            else:
                status['mode'] = 'Demo'
                
        except Exception as e:
            logging.error(f"Error parsing trading status: {e}")
            
        self.current_status = status
        self.last_updated = datetime.now()
        return status
    
    def get_current_status(self):
        """Get current trading status"""
        if not self.current_status:
            return self.parse_status_from_logs()
        return self.current_status
    
    def get_mode_indicator(self):
        """Get trading mode with color indicator"""
        status = self.get_current_status()
        mode = status.get('mode', 'Demo')
        
        if mode == 'Live':
            return {
                'mode': 'Live Trading',
                'color': 'success',
                'icon': 'fa-broadcast-tower',
                'status': 'Active'
            }
        else:
            return {
                'mode': 'Demo Trading',
                'color': 'warning', 
                'icon': 'fa-flask',
                'status': 'Simulation'
            }
    
    def get_container_status_summary(self):
        """Get container status summary"""
        status = self.get_current_status()
        
        buy_running = status.get('buy_container_running', False)
        sell_running = status.get('sell_container_running', False)
        
        return {
            'buy_container': {
                'running': buy_running,
                'status': 'Running' if buy_running else 'Stopped',
                'color': 'success' if buy_running else 'secondary'
            },
            'sell_container': {
                'running': sell_running,
                'status': 'Running' if sell_running else 'Stopped',
                'color': 'success' if sell_running else 'secondary'
            }
        }
    
    def get_trading_counts(self):
        """Get formatted trading counts"""
        status = self.get_current_status()
        
        return {
            'demo_counts': {
                'buy_success': status.get('buy_success_count', 0),
                'buy_stop_loss': status.get('buy_stop_loss_count', 0),
                'sell_success': status.get('sell_success_count', 0),
                'sell_stop_loss': status.get('sell_stop_loss_count', 0)
            },
            'live_counts': {
                'success': status.get('live_trade_success_count', 0),
                'failure': status.get('live_trade_failure_count', 0)
            }
        }
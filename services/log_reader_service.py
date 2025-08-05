import docker
import logging
import re
from datetime import datetime
from typing import List, Dict, Optional

class LogReaderService:
    def __init__(self):
        try:
            self.client = docker.from_env()
        except Exception as e:
            logging.error(f"Failed to connect to Docker: {e}")
            self.client = None
    
    def get_log_reader_logs(self, lines: int = 100) -> List[Dict]:
        """
        Get logs from the log-reader container and parse them into structured data
        """
        if not self.client:
            return []
        
        try:
            container = self.client.containers.get('log-reader')
            if container.status != 'running':
                return []
            
            # Get recent logs
            logs = container.logs(tail=lines, timestamps=True).decode('utf-8')
            return self._parse_strategy_logs(logs)
            
        except Exception as e:
            logging.error(f"Error reading log-reader container logs: {e}")
            return []
    
    def _parse_strategy_logs(self, logs: str) -> List[Dict]:
        """
        Parse the strategy manager logs into structured data
        """
        parsed_logs = []
        lines = logs.strip().split('\n')
        
        current_status = {}
        
        for line in lines:
            if not line.strip():
                continue
            
            try:
                # Extract timestamp and message
                timestamp_match = re.match(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z)\s+(.+)$', line)
                if timestamp_match:
                    timestamp_str = timestamp_match.group(1)
                    message = timestamp_match.group(2)
                else:
                    # Fallback for logs without Docker timestamp
                    message = line
                    timestamp_str = datetime.utcnow().isoformat() + 'Z'
                
                # Parse different log types
                log_entry = self._parse_log_message(message, timestamp_str)
                if log_entry:
                    parsed_logs.append(log_entry)
                    
                    # Update current status if it's a status entry
                    if log_entry['type'] == 'status_update':
                        current_status.update(log_entry.get('data', {}))
                        
            except Exception as e:
                logging.error(f"Error parsing log line: {line}, error: {e}")
                continue
        
        # Add current status as the latest entry if we have it
        if current_status:
            parsed_logs.append({
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'type': 'current_status',
                'message': 'Current Trading Status',
                'data': current_status,
                'level': 'info'
            })
        
        return sorted(parsed_logs, key=lambda x: x['timestamp'], reverse=True)
    
    def _parse_log_message(self, message: str, timestamp: str) -> Optional[Dict]:
        """
        Parse individual log messages into structured format
        """
        log_entry = {
            'timestamp': timestamp,
            'raw_message': message,
            'level': 'info'
        }
        
        # Remove timestamp prefix if present in message
        message = re.sub(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} - ', '', message)
        
        # Parse different message types
        if '🔴 Containers detected running - DISABLING API calls' in message:
            log_entry.update({
                'type': 'system_alert',
                'message': 'Containers detected - API calls disabled',
                'level': 'warning',
                'icon': 'exclamation-triangle'
            })
            
        elif 'Starting Trading Strategy Manager' in message:
            log_entry.update({
                'type': 'system_start',
                'message': 'Trading Strategy Manager started',
                'level': 'success',
                'icon': 'play-circle'
            })
            
        elif '🔄 LIVE TRADING DETECTED' in message:
            log_entry.update({
                'type': 'trading_mode',
                'message': 'Live trading mode activated',
                'level': 'info',
                'icon': 'broadcast-pin'
            })
            
        elif '🚀 Live trading detected' in message:
            log_entry.update({
                'type': 'monitoring_start',
                'message': 'Live trading monitoring started',
                'level': 'success',
                'icon': 'rocket'
            })
            
        elif '=== Current Status ===' in message:
            log_entry.update({
                'type': 'status_header',
                'message': 'Status Report',
                'level': 'info',
                'icon': 'info-circle'
            })
            
        elif self._is_status_line(message):
            status_data = self._parse_status_line(message)
            if status_data:
                log_entry.update({
                    'type': 'status_update',
                    'message': f"{status_data['key']}: {status_data['value']}",
                    'data': {status_data['key']: status_data['value']},
                    'level': 'info',
                    'icon': 'info'
                })
                
        else:
            log_entry.update({
                'type': 'general',
                'message': message,
                'level': 'info',
                'icon': 'info'
            })
        
        return log_entry
    
    def _is_status_line(self, message: str) -> bool:
        """Check if the message is a status line"""
        status_patterns = [
            r'BUY Coins Tracking:',
            r'SELL Coins Tracking:',
            r'BUY Success Count:',
            r'BUY Stop Loss Count:',
            r'SELL Success Count:',
            r'SELL Stop Loss Count:',
            r'Live Trade Success Count:',
            r'Live Trade Failure Count:',
            r'BUY Container Running:',
            r'SELL Container Running:',
            r'Waiting for BUY start:',
            r'Waiting for SELL start:',
            r'API Calls Enabled:',
            r'Weekly Reset In Progress:',
            r'Current IST Time:',
            r'Next Weekly Reset:'
        ]
        
        return any(re.search(pattern, message) for pattern in status_patterns)
    
    def _parse_status_line(self, message: str) -> Optional[Dict]:
        """Parse status line into key-value pair"""
        match = re.match(r'^(.+?):\s*(.+)$', message)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            return {'key': key, 'value': value}
        return None
    
    def get_trading_summary(self) -> Dict:
        """
        Get a summary of current trading status from logs
        """
        logs = self.get_log_reader_logs(lines=50)
        
        summary = {
            'status': 'unknown',
            'api_enabled': False,
            'buy_container_running': False,
            'sell_container_running': False,
            'live_trades_success': 0,
            'live_trades_failure': 0,
            'last_update': None
        }
        
        # Extract latest status information
        for log in logs:
            if log.get('type') == 'status_update' and log.get('data'):
                data = log['data']
                key = list(data.keys())[0] if data else None
                value = list(data.values())[0] if data else None
                
                if key == 'API Calls Enabled':
                    summary['api_enabled'] = value.lower() == 'true'
                elif key == 'BUY Container Running':
                    summary['buy_container_running'] = value.lower() == 'true'
                elif key == 'SELL Container Running':
                    summary['sell_container_running'] = value.lower() == 'true'
                elif key == 'Live Trade Success Count':
                    try:
                        summary['live_trades_success'] = int(value)
                    except ValueError:
                        pass
                elif key == 'Live Trade Failure Count':
                    try:
                        summary['live_trades_failure'] = int(value)
                    except ValueError:
                        pass
                elif key == 'Current IST Time':
                    summary['last_update'] = value
        
        # Determine overall status
        if summary['buy_container_running'] or summary['sell_container_running']:
            summary['status'] = 'active'
        else:
            summary['status'] = 'inactive'
            
        return summary
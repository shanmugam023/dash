import logging
from datetime import datetime
from services.live_trading_simulator import live_simulator

class DockerMonitor:
    def __init__(self):
        # For Replit compatibility, we'll simulate container status
        self.client = None
        logging.info("Docker not available in Replit - using trading simulation")
    
    def _initialize_docker_client(self):
        """Initialize Docker client with fallback methods"""
        try:
            # Method 1: Try environment variables
            client = docker.from_env()
            # Test connection
            client.ping()
            logging.info("Docker connection successful using environment")
            return client
        except Exception as e1:
            logging.warning(f"Docker from_env failed: {e1}")
            
            try:
                # Method 2: Try Unix socket directly
                client = docker.DockerClient(base_url='unix://var/run/docker.sock')
                client.ping()
                logging.info("Docker connection successful using Unix socket")
                return client
            except Exception as e2:
                logging.warning(f"Docker Unix socket failed: {e2}")
                
                try:
                    # Method 3: Try TCP connection (if Docker API is exposed)
                    client = docker.DockerClient(base_url='tcp://localhost:2376')
                    client.ping()
                    logging.info("Docker connection successful using TCP")
                    return client
                except Exception as e3:
                    logging.error(f"All Docker connection methods failed: {e1}, {e2}, {e3}")
                    raise e3

    def get_container_status(self):
        """Get simulated container status for Replit"""
        containers_info = []
        
        target_containers = [
            'Yuva_Positions_trading_bot',
            'Shan_Positions_trading_bot',
            'log-reader'
        ]
        
        try:
            # Simulate container status for Replit
            for container_name in target_containers:
                status_info = {
                    'name': container_name,
                    'status': 'running',
                    'id': 'simulated',
                    'image': 'trading-bot:latest',
                    'created': datetime.utcnow().isoformat(),
                    'uptime': 'Live simulation active'
                }
                containers_info.append(status_info)
                    
                    # Update database
                    self._update_container_status(container_name, container.status, status_info['uptime'])
            
            # Add missing containers as offline
            found_names = [c['name'] for c in containers_info]
            for target in target_containers:
                if target not in found_names:
                    containers_info.append({
                        'name': target,
                        'status': 'not_found',
                        'id': 'N/A',
                        'image': 'N/A',
                        'created': 'N/A',
                        'uptime': 'N/A'
                    })
                    self._update_container_status(target, 'not_found', 'N/A')
                    
        except Exception as e:
            logging.error(f"Error getting container status: {e}")
        
        return containers_info

    def _calculate_uptime(self, container):
        """Calculate container uptime"""
        try:
            if container.status != 'running':
                return 'Not running'
            
            started_at = container.attrs['State']['StartedAt']
            started_time = datetime.fromisoformat(started_at.replace('Z', '+00:00'))
            uptime = datetime.now(started_time.tzinfo) - started_time
            
            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            
            if days > 0:
                return f"{days}d {hours}h {minutes}m"
            elif hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"
                
        except Exception as e:
            logging.error(f"Error calculating uptime: {e}")
            return "Unknown"

    def _update_container_status(self, name, status, uptime):
        """Update container status in database"""
        try:
            container_status = ContainerStatus.query.filter_by(container_name=name).first()
            if container_status:
                container_status.status = status
                container_status.uptime = uptime
                container_status.last_updated = datetime.utcnow()
            else:
                container_status = ContainerStatus(
                    container_name=name,
                    status=status,
                    uptime=uptime
                )
                db.session.add(container_status)
            
            db.session.commit()
        except Exception as e:
            logging.error(f"Error updating container status: {e}")
            db.session.rollback()

    def update_container_status(self):
        """Update all container statuses"""
        return self.get_container_status()

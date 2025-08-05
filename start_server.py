#!/usr/bin/env python3
"""
Trading Dashboard Server Startup Script
Runs the trading dashboard on Ubuntu server with port 24242
"""

import os
import sys
import logging
from app import app, db

def setup_logging():
    """Configure logging for production"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('/var/log/trading-dashboard/app.log'),
            logging.StreamHandler()
        ]
    )

def initialize_database():
    """Initialize SQLite database"""
    try:
        with app.app_context():
            db.create_all()
            logging.info("✅ Database initialized successfully")
            return True
    except Exception as e:
        logging.error(f"❌ Database initialization failed: {e}")
        return False

def check_docker_containers():
    """Check if required Docker containers are available"""
    import docker
    try:
        client = docker.from_env()
        required_containers = [
            'Yuva_Positions_trading_bot',
            'Shan_Positions_trading_bot', 
            'log-reader'
        ]
        
        running_containers = [c.name for c in client.containers.list()]
        all_containers = [c.name for c in client.containers.list(all=True)]
        
        logging.info("🐳 Docker Container Status:")
        for container in required_containers:
            if container in running_containers:
                logging.info(f"  ✅ {container}: Running")
            elif container in all_containers:
                logging.warning(f"  ⚠️  {container}: Stopped")
            else:
                logging.warning(f"  ❌ {container}: Not found")
                
    except Exception as e:
        logging.warning(f"⚠️  Could not check Docker containers: {e}")

def main():
    """Main server startup"""
    print("🚀 Starting Trading Dashboard Server")
    print("=====================================")
    
    # Setup logging
    setup_logging()
    
    # Initialize database
    if not initialize_database():
        sys.exit(1)
    
    # Check Docker containers
    check_docker_containers()
    
    # Display startup information
    logging.info("🌐 Server starting on http://0.0.0.0:24242")
    logging.info("📊 Dashboard URL: http://YOUR_SERVER_IP:24242")
    logging.info("🗄️  Database: SQLite (trading_dashboard.db)")
    logging.info("🐳 Monitoring containers: Yuva_Positions_trading_bot, Shan_Positions_trading_bot, log-reader")
    
    # Start the server
    try:
        app.run(host='0.0.0.0', port=24242, debug=False)
    except KeyboardInterrupt:
        logging.info("🛑 Server stopped by user")
    except Exception as e:
        logging.error(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
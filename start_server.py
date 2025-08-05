#!/usr/bin/env python3
"""
Trading Dashboard Server Startup Script
This script starts the trading dashboard on port 24242 for Ubuntu server deployment
"""

import os
import sys
import subprocess
import signal
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if all required packages are installed"""
    try:
        import flask
        import gunicorn
        import psycopg2
        import docker
        logger.info("All dependencies are available")
        return True
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        return False

def check_database():
    """Check database connectivity"""
    try:
        from app import db, app
        with app.app_context():
            db.create_all()
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

def check_port(port=24242):
    """Check if port is available"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', port))
            logger.info(f"Port {port} is available")
            return True
        except OSError:
            logger.error(f"Port {port} is already in use")
            return False

def start_production_server():
    """Start the production server using gunicorn"""
    logger.info("Starting Trading Dashboard in production mode on port 24242...")
    
    # Check all prerequisites
    if not check_dependencies():
        logger.error("Cannot start server: missing dependencies")
        sys.exit(1)
    
    if not check_database():
        logger.error("Cannot start server: database connection failed")
        sys.exit(1)
    
    if not check_port():
        logger.error("Cannot start server: port 24242 is in use")
        sys.exit(1)
    
    # Set environment variables
    os.environ['FLASK_ENV'] = 'production'
    os.environ['PYTHONPATH'] = str(Path.cwd())
    
    # Gunicorn command
    cmd = [
        'gunicorn',
        '--config', 'gunicorn_config.py',
        '--bind', '0.0.0.0:24242',
        '--workers', '4',
        '--worker-class', 'sync',
        '--timeout', '30',
        '--keepalive', '2',
        '--max-requests', '1000',
        '--max-requests-jitter', '100',
        '--preload',
        '--access-logfile', '-',
        '--error-logfile', '-',
        '--log-level', 'info',
        'main:app'
    ]
    
    try:
        # Start the server
        logger.info("Executing: " + ' '.join(cmd))
        process = subprocess.Popen(cmd)
        
        # Handle shutdown gracefully
        def signal_handler(signum, frame):
            logger.info("Received shutdown signal, stopping server...")
            process.terminate()
            process.wait()
            logger.info("Server stopped")
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        logger.info("Trading Dashboard is running on http://0.0.0.0:24242")
        logger.info("Press Ctrl+C to stop the server")
        
        # Wait for the process to complete
        process.wait()
        
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)

def start_development_server():
    """Start the development server"""
    logger.info("Starting Trading Dashboard in development mode on port 24242...")
    
    if not check_dependencies():
        logger.error("Cannot start server: missing dependencies")
        sys.exit(1)
    
    if not check_database():
        logger.error("Cannot start server: database connection failed")
        sys.exit(1)
    
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    
    try:
        from main import app
        app.run(host='0.0.0.0', port=24242, debug=True)
    except Exception as e:
        logger.error(f"Failed to start development server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--dev':
        start_development_server()
    else:
        start_production_server()
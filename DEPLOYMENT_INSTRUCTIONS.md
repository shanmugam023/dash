# Trading Dashboard - Ubuntu Server Deployment

## Overview
This trading dashboard monitors Docker containers and provides real-time trading analytics. It's configured to run on **Ubuntu server with port 24242** and uses an **embedded SQLite database** (no separate database server required).

## Quick Deployment

### 1. Prerequisites
- Ubuntu server with Docker installed
- Python 3.8+ available
- The following Docker containers running:
  - `Yuva_Positions_trading_bot`
  - `Shan_Positions_trading_bot` 
  - `log-reader`

### 2. Automated Setup
```bash
# Clone or copy the project to your server
cd /path/to/trading-dashboard

# Make deployment script executable
chmod +x ubuntu_deploy.sh

# Run the deployment script
./ubuntu_deploy.sh
```

### 3. Manual Setup (Alternative)
```bash
# Install dependencies
sudo apt update && sudo apt install -y python3 python3-pip python3-venv docker.io

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install flask flask-sqlalchemy gunicorn docker python-dotenv sqlalchemy werkzeug

# Initialize database
python3 -c "from app import app, db; app.app_context().push(); db.create_all()"

# Start the server
python3 start_server.py
```

## Configuration Details

### Port Configuration
- **Application Port**: 24242
- **Access URL**: `http://YOUR_SERVER_IP:24242`
- **Firewall**: Allow port 24242/tcp

### Database Configuration  
- **Type**: SQLite (embedded)
- **File**: `trading_dashboard.db`
- **Location**: Same directory as application
- **No external database server required**

### Docker Containers Monitored
The application specifically monitors these 3 containers:
1. `Yuva_Positions_trading_bot`
2. `Shan_Positions_trading_bot`
3. `log-reader`

## Service Management

### Using Systemd (Recommended)
```bash
# Check service status
sudo systemctl status trading-dashboard

# Start service
sudo systemctl start trading-dashboard

# Stop service
sudo systemctl stop trading-dashboard

# Restart service
sudo systemctl restart trading-dashboard

# View logs
sudo journalctl -u trading-dashboard -f
```

### Manual Start
```bash
# Production mode with Gunicorn
gunicorn --config gunicorn_config.py main:app

# Development mode
python3 start_server.py

# Direct Flask run
python3 app.py
```

## Troubleshooting

### Common Issues

1. **Port 24242 not accessible**
   ```bash
   # Allow through firewall
   sudo ufw allow 24242/tcp
   sudo ufw enable
   ```

2. **Docker containers not found**
   ```bash
   # Check container names
   docker ps -a --format "table {{.Names}}\t{{.Status}}"
   
   # Start required containers
   docker start Yuva_Positions_trading_bot
   docker start Shan_Positions_trading_bot
   docker start log-reader
   ```

3. **Database issues**
   ```bash
   # Recreate database
   rm -f trading_dashboard.db
   python3 -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

4. **Permission errors**
   ```bash
   # Fix file permissions
   chmod +x *.py *.sh
   chown $USER:$USER trading_dashboard.db
   ```

### Log Locations
- **Application logs**: `/var/log/trading-dashboard/app.log` (systemd)
- **System logs**: `sudo journalctl -u trading-dashboard -f`
- **Gunicorn logs**: Console output or configured log files

## Features

### Dashboard Sections
1. **Trading Performance**: Individual P&L for Yuva and Shan
2. **Trading Strategy Logs**: Real-time container logs with filtering
3. **Long vs Short Performance**: Compact chart showing performance comparison
4. **Container Status**: Status of all 3 monitored containers

### User Controls
- **User Selection**: Filter view by All Users, Yuva, or Shan
- **Log Filtering**: Filter logs by All, System, Trading, or Status
- **Real-time Updates**: Auto-refresh functionality
- **Container Monitoring**: Live status of Docker containers

## File Structure
```
trading-dashboard/
├── app.py                    # Main Flask application
├── main.py                   # Application entry point
├── start_server.py           # Ubuntu server startup script
├── ubuntu_deploy.sh          # Automated deployment script
├── gunicorn_config.py        # Gunicorn production configuration
├── models.py                 # Database models
├── routes.py                 # API routes
├── trading_dashboard.db      # SQLite database (created automatically)
├── templates/                # HTML templates
├── static/                   # CSS, JS, assets
└── services/                 # Background services
    ├── docker_monitor.py     # Docker container monitoring
    └── log_reader_service.py # Log processing service
```

## Security Notes
- SQLite database is embedded (no network database exposure)
- Application binds to 0.0.0.0:24242 (configure firewall appropriately)
- Docker socket access required for container monitoring
- Run with appropriate user permissions (not root)

## Support
For issues or questions about deployment:
1. Check the logs: `sudo journalctl -u trading-dashboard -f`
2. Verify Docker containers are running: `docker ps`
3. Confirm port 24242 is accessible: `telnet YOUR_SERVER_IP 24242`
4. Check database file exists and has correct permissions
# Ubuntu Server Docker Connection Fix

## Problem
The trading dashboard shows old/static logs instead of live container logs because Docker connection is failing on the Ubuntu server.

## Solution Steps

### 1. Fix Docker Permissions (Run on Ubuntu Server)

```bash
# Navigate to your trading dashboard directory
cd /opt/trading-dashboard

# Fix Docker socket permissions
sudo chmod 666 /var/run/docker.sock

# Add your user to docker group  
sudo usermod -aG docker $USER

# Log out and log back in for group changes to take effect
```

### 2. Test Docker Connection

```bash
# Run the Docker fix script
python3 docker_fix.py

# This will:
# - Test Docker connection
# - List all containers
# - Verify your 3 target containers are found
```

### 3. Test Live Log Streaming

```bash
# Run the live logs test
python3 fix_live_logs.py

# This will:
# - Test live log streaming from each container
# - Show sample logs from each container
# - Verify logs are updating in real-time
```

### 4. Restart the Application

```bash
# If using systemd service
sudo systemctl restart trading-dashboard

# Or if running manually
cd /opt/trading-dashboard
source venv/bin/activate
python3 start_server.py
```

### 5. Verify Fix

1. Open your browser: `http://YOUR_SERVER_IP:24242`
2. Check the logs section - should now show live, updating logs
3. User stats should display correctly (no more database errors)
4. Container status should show "running" for all 3 containers

## Expected Container Names
- `Yuva_Positions_trading_bot`
- `Shan_Positions_trading_bot`  
- `log-reader`

## Troubleshooting

### If Docker connection still fails:
```bash
# Check Docker service status
sudo systemctl status docker

# Start Docker if stopped
sudo systemctl start docker

# Check your user is in docker group
groups $USER

# Should show "docker" in the list
```

### If containers are not found:
```bash
# List all containers
docker ps -a

# Start containers if they're stopped
docker start Yuva_Positions_trading_bot
docker start Shan_Positions_trading_bot  
docker start log-reader
```

### If logs are still not live:
```bash
# Check if containers are actually producing logs
docker logs -f Yuva_Positions_trading_bot

# Should show live, updating logs
# If not, the containers themselves aren't generating new logs
```

## Files Modified
- `services/docker_monitor.py` - Enhanced Docker connection with fallback methods
- `services/log_reader_service.py` - Improved log parsing and live streaming
- `docker_fix.py` - New diagnostic and fix script
- `fix_live_logs.py` - New live log testing script

The application will now connect properly to your Docker containers and display live, real-time logs from your trading bots.
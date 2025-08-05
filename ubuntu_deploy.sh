#!/bin/bash

# Trading Dashboard Ubuntu Server Deployment Script
# This script sets up the trading dashboard to run on Ubuntu server with port 24242

echo "🚀 Trading Dashboard Ubuntu Deployment Setup"
echo "============================================="

# Check if running as root

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and required system packages
echo "🐍 Installing Python and dependencies..."
sudo apt install -y python3 python3-pip python3-venv git docker.io

# Add user to docker group
echo "🐳 Adding user to docker group..."
sudo usermod -aG docker $USER

# Create application directory
APP_DIR="/opt/trading-dashboard"
echo "📁 Creating application directory: $APP_DIR"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Copy application files (assuming script is run from project directory)
echo "📋 Copying application files..."
cp -r . $APP_DIR/
cd $APP_DIR

# Create Python virtual environment
echo "🔧 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install flask flask-sqlalchemy gunicorn docker python-dotenv sqlalchemy werkzeug

# Create systemd service file
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/trading-dashboard.service > /dev/null <<EOF
[Unit]
Description=Trading Dashboard Application
After=network.target docker.service
Requires=docker.service

[Service]
Type=notify
User=$USER
Group=$USER
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/gunicorn --config gunicorn_config.py main:app
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Create log directory
sudo mkdir -p /var/log/trading-dashboard
sudo chown $USER:$USER /var/log/trading-dashboard

# Set correct permissions
chmod +x $APP_DIR/ubuntu_deploy.sh
chmod 644 $APP_DIR/*.py

# Initialize database
echo "🗄️ Initializing SQLite database..."
python3 -c "from app import app, db; app.app_context().push(); db.create_all(); print('✅ Database initialized')"

# Enable and start service
echo "🔄 Enabling and starting service..."
sudo systemctl daemon-reload
sudo systemctl enable trading-dashboard.service
sudo systemctl start trading-dashboard.service

# Check service status
echo "📊 Service Status:"
sudo systemctl status trading-dashboard.service --no-pager

# Display firewall instructions
echo ""
echo "🔥 FIREWALL CONFIGURATION:"
echo "To allow access to port 24242, run:"
echo "sudo ufw allow 24242/tcp"
echo "sudo ufw enable"

# Display completion message
echo ""
echo "✅ DEPLOYMENT COMPLETE!"
echo "=============================="
echo "🌐 Application URL: http://YOUR_SERVER_IP:24242"
echo "📊 Service Status: sudo systemctl status trading-dashboard"
echo "📝 View Logs: sudo journalctl -u trading-dashboard -f"
echo "🔄 Restart Service: sudo systemctl restart trading-dashboard"
echo "🛑 Stop Service: sudo systemctl stop trading-dashboard"
echo ""
echo "⚠️  IMPORTANT:"
echo "1. Make sure Docker containers are running:"
echo "   - Yuva_Positions_trading_bot"
echo "   - Shan_Positions_trading_bot"
echo "   - log-reader"
echo "2. Allow port 24242 in your firewall"
echo "3. Database file: $APP_DIR/trading_dashboard.db"
echo ""
echo "🎉 Your trading dashboard is ready!"

#!/bin/bash

# Trading Dashboard Service Setup Script
# This script sets up the trading dashboard as a systemd service

echo "🚀 Setting up Trading Dashboard Service..."

# Get current directory
CURRENT_DIR=$(pwd)
USER=$(whoami)

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: Please run this script from the trading dashboard directory"
    exit 1
fi

# Create systemd service file
echo "📝 Creating systemd service file..."
sudo tee /etc/systemd/system/trading-dashboard.service > /dev/null <<EOF
[Unit]
Description=Trading Dashboard - Binance Trading Analytics
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=exec
User=$USER
Group=$USER
WorkingDirectory=$CURRENT_DIR
Environment=PATH=$CURRENT_DIR/venv/bin
Environment=DATABASE_URL=postgresql://trading_user:Redshan%40123@localhost/trading_dashboard
Environment=SESSION_SECRET=your_secret_key_here_make_it_long_and_random
Environment=FLASK_ENV=production
ExecStart=$CURRENT_DIR/venv/bin/python start_server.py
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Service file created at /etc/systemd/system/trading-dashboard.service"

# Reload systemd
echo "🔄 Reloading systemd daemon..."
sudo systemctl daemon-reload

# Enable the service
echo "🔧 Enabling trading dashboard service..."
sudo systemctl enable trading-dashboard

echo "✅ Trading Dashboard service setup complete!"
echo ""
echo "📋 Available commands:"
echo "  Start service:    sudo systemctl start trading-dashboard"
echo "  Stop service:     sudo systemctl stop trading-dashboard"
echo "  Restart service:  sudo systemctl restart trading-dashboard"
echo "  Check status:     sudo systemctl status trading-dashboard"
echo "  View logs:        sudo journalctl -u trading-dashboard -f"
echo ""
echo "🌐 After starting, your dashboard will be available at:"
echo "  http://localhost:24242"
echo ""
echo "⚠️  Remember to:"
echo "  1. Update the DATABASE_URL in the service file with your actual database credentials"
echo "  2. Update the SESSION_SECRET with a secure random string"
echo "  3. Ensure PostgreSQL is running: sudo systemctl start postgresql"
echo "  4. Configure firewall if needed: sudo ufw allow 24242"

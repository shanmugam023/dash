#!/bin/bash

# Quick Start Script for Trading Dashboard
# Run this script to quickly set up and start the dashboard

echo "🚀 Trading Dashboard Quick Start"
echo "================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install flask flask-sqlalchemy gunicorn psycopg2-binary python-dotenv docker werkzeug

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://trading_user:your_password@localhost/trading_dashboard

# Security
SESSION_SECRET=your_secret_key_here_make_it_long_and_random

# Application
FLASK_ENV=production
FLASK_DEBUG=0
EOF
    echo "⚠️  Please edit .env file with your actual database credentials!"
fi

# Check if PostgreSQL is running
if systemctl is-active --quiet postgresql; then
    echo "✅ PostgreSQL is running"
else
    echo "⚠️  PostgreSQL is not running. Starting it now..."
    sudo systemctl start postgresql
fi

echo ""
echo "🎯 Choose how to run the dashboard:"
echo "1. Development mode (with auto-reload)"
echo "2. Production mode (with gunicorn)"
echo "3. Setup as system service"
echo ""
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo "🚀 Starting in development mode..."
        python main.py
        ;;
    2)
        echo "🚀 Starting in production mode..."
        python start_server.py
        ;;
    3)
        echo "🔧 Setting up as system service..."
        chmod +x setup_service.sh
        ./setup_service.sh
        echo ""
        read -p "Do you want to start the service now? (y/n): " start_service
        if [ "$start_service" = "y" ] || [ "$start_service" = "Y" ]; then
            sudo systemctl start trading-dashboard
            echo "✅ Service started! Check status with: sudo systemctl status trading-dashboard"
        fi
        ;;
    *)
        echo "❌ Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "🌐 Dashboard will be available at:"
echo "   http://localhost:24242"
echo ""
echo "📊 Features:"
echo "   ✓ Phoenix-style professional interface"
echo "   ✓ Long vs Short position comparison"  
echo "   ✓ Real-time trading data"
echo "   ✓ Performance analytics"
echo "   ✓ Bot status monitoring"
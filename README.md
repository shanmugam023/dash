# Enhanced Trading Dashboard

A comprehensive real-time trading dashboard for monitoring Binance trading bots with advanced analytics, trade history, and performance tracking.

## Features

### 🚀 Core Features
- **Real-time Container Monitoring**: Track Docker containers running trading bots
- **Comprehensive Trade Analytics**: Detailed statistics for multiple traders (Yuva & Shan)
- **Enhanced Trade History**: Complete trade history with filtering by time periods
- **Advanced Performance Metrics**: Win rates, profit factors, P&L analysis
- **Professional Dashboard Design**: Modern, responsive UI with dark theme
- **PostgreSQL Database**: Robust data storage with proper indexing

### 📊 Analytics Features
- **Period-based Analysis**: View stats by day, week, month, year, or all-time
- **Long vs Short Comparison**: Separate tracking for LONG and SHORT positions
- **Real-time P&L Calculation**: Live unrealized and realized P&L tracking
- **Success/Failure Rates**: Detailed win/loss statistics
- **Interactive Charts**: Performance comparison and distribution charts

### 🔧 Technical Features
- **Enhanced Log Parsing**: Advanced log processing from trading bot containers
- **API Endpoints**: RESTful APIs for data access
- **Auto-refresh**: Real-time data updates every 30 seconds
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Production Ready**: Configured for Ubuntu server deployment

## Installation & Setup

### Prerequisites
- Python 3.11+
- PostgreSQL database
- Docker (for container monitoring)
- Ubuntu Server (recommended for production)

### Quick Start

1. **Clone and Setup**
   ```bash
   git clone <repository>
   cd trading-dashboard
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   ```bash
   export DATABASE_URL="postgresql://user:pass@localhost/trading_db"
   export SESSION_SECRET="your-secret-key"
   ```

3. **Start Development Server (Port 5000)**
   ```bash
   python start_server.py --dev
   ```

4. **Start Production Server**
   ```bash
   python start_server.py
   ```

### Ubuntu Server Deployment (Port 24242)

For Ubuntu server deployment on port 24242, modify the configuration files:
- Update `gunicorn_config.py` bind setting to `"0.0.0.0:24242"`
- Update `start_server.py` port references from 5000 to 24242
- Then run the production server

### Production Deployment on Ubuntu

1. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv postgresql postgresql-contrib docker.io
   ```

2. **Setup Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Database**
   ```bash
   sudo -u postgres createdb trading_dashboard
   sudo -u postgres createuser trading_user
   ```

4. **Start Production Server**
   ```bash
   python start_server.py
   ```

The dashboard will be available at `http://your-server:24242`

## API Endpoints

### Core Endpoints
- `GET /` - Main dashboard
- `GET /api/container-status` - Container status information
- `GET /api/trading-stats` - Trading statistics for both users
- `GET /api/logs` - Recent log entries
- `GET /api/refresh-data` - Refresh all data

### Enhanced Endpoints
- `GET /api/trade-history/<period>` - Trade history by period (today, week, month, year, all)
- `GET /api/statistics/<user>/<period>` - User statistics by period
- `GET /api/positions/current` - Current open positions

## Configuration

### Server Configuration
- **Port**: 24242 (configurable in `gunicorn_config.py`)
- **Workers**: 4 (configurable)
- **Timeout**: 30 seconds
- **Max Requests**: 1000 per worker

### Database Schema
The dashboard uses PostgreSQL with the following main tables:
- `trading_session` - Individual trades and positions
- `trading_stats` - Aggregated statistics by user and period
- `container_status` - Docker container monitoring data

### Container Monitoring
Monitors these Docker containers:
- `Yuva_Positions_trading_bot` - Yuva's trading bot
- `Shan_Positions_trading_bot` - Shan's trading bot
- `log-reader` - Log processing container

## Usage

### Dashboard Features

1. **Overview Cards**: Total trades, success/failure rates, and overall P&L
2. **Time Period Filters**: Filter data by Today, This Week, This Month, This Year, or All Time
3. **User Comparison**: Side-by-side comparison of Yuva and Shan performance
4. **Current Positions**: Real-time view of open positions with live P&L
5. **Trade History**: Complete trade history with filtering options
6. **Performance Charts**: Visual comparison of trading performance
7. **Container Status**: Real-time monitoring of trading bot containers

### Key Metrics Tracked
- **Total Trades**: Complete count of all trading sessions
- **Success/Failure Rates**: Win/loss percentages
- **Long vs Short Performance**: Separate tracking for position types
- **Profit Factor**: Ratio of total profits to total losses
- **Average Win/Loss**: Mean profit and loss amounts
- **Win Rate**: Percentage of profitable trades
- **Unrealized P&L**: Live profit/loss for open positions
- **Realized P&L**: Profit/loss for closed positions

## Log Processing

The dashboard automatically processes logs from trading bot containers to:
- Extract position information (symbol, side, entry price, size)
- Calculate real-time P&L
- Track price movements
- Monitor position status
- Update trade statistics

### Supported Log Formats
The log parser recognizes these patterns:
- Position management: `📈 Managing LONG/SHORT position for SYMBOL:`
- Entry prices: `Entry Price: X.XXXX`
- Current prices: `Current Price: X.XXXX`
- Position sizes: `Position Size: XXX.X`
- Price movements: `Price Movement: X.XX%`

## Troubleshooting

### Common Issues

1. **Port 24242 in use**
   ```bash
   sudo lsof -i :24242
   sudo kill -9 <PID>
   ```

2. **Database connection issues**
   - Check DATABASE_URL environment variable
   - Verify PostgreSQL is running
   - Check database credentials

3. **Docker connection issues**
   - Ensure Docker daemon is running
   - Check user permissions for Docker socket
   - Verify container names match configuration

4. **Missing dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Logs
Server logs are written to stdout/stderr. For production deployment, consider using:
- `systemd` for service management
- `logrotate` for log rotation
- `nginx` as reverse proxy

## Development

### Project Structure
```
trading-dashboard/
├── app.py                 # Flask application setup
├── main.py               # Application entry point
├── routes.py             # API routes and endpoints
├── models.py             # Database models
├── gunicorn_config.py    # Production server configuration
├── start_server.py       # Server startup script
├── services/             # Business logic services
├── templates/            # Jinja2 templates
├── static/              # CSS, JS, and assets
└── README.md            # This file
```

### Adding New Features
1. Update database models in `models.py`
2. Add business logic in `services/`
3. Create API endpoints in `routes.py`
4. Update templates for UI changes
5. Test with both development and production configurations

## License

This project is proprietary software for trading bot monitoring and analytics.

## Support

For issues and feature requests, please contact the development team.
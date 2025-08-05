# Enhanced Trading Dashboard

## Overview

This is a comprehensive real-time trading dashboard built with Flask that monitors Docker containers running Binance trading bots for two users (Yuva and Shan). The enhanced system includes advanced trade history storage, period-based analytics (daily, weekly, monthly, yearly), professional UI design, and runs on port 24242 for Ubuntu server deployment. The dashboard provides detailed performance comparisons, interactive charts, comprehensive trade filtering, and real-time P&L calculations with PostgreSQL database storage.

## User Preferences

Preferred communication style: Simple, everyday language.
Preferred deployment: Ubuntu server on port 24242
Design preference: Clean, professional dashboard with good looks
Data requirements: Store all trade history with period-based comparisons

## System Architecture

### Backend Architecture
- **Flask Web Framework**: Core web application using Flask with SQLAlchemy ORM for PostgreSQL database operations
- **Enhanced Service Layer**: Advanced services for Docker monitoring, enhanced log parsing, and comprehensive trading analytics
- **Enhanced Database Models**: Extended SQLAlchemy models with trade history, period-based statistics, and performance indexing
- **Extended RESTful API**: JSON endpoints for real-time data, period-based filtering, and trade history access
- **Production Configuration**: Gunicorn server setup with multi-worker configuration for Ubuntu deployment

### Frontend Architecture
- **Bootstrap 5 UI**: Modern responsive design with dark theme optimized for trading environments
- **Real-time Updates**: JavaScript-based auto-refresh functionality with 30-second intervals
- **Interactive Charts**: Chart.js integration for visualizing trading performance and metrics
- **Component-based Templates**: Jinja2 templating with base template inheritance

### Data Storage
- **PostgreSQL Database**: Production-ready database with connection pooling and automatic schema creation
- **Enhanced Trading Session Tracking**: Extended position tracking with realized/unrealized P&L, trade types, and strategy notes
- **Period-based Statistics**: Daily, weekly, monthly, and yearly aggregated statistics with separate long/short tracking
- **Trade History Storage**: Complete historical data with advanced filtering and period-based comparisons
- **Performance Analytics**: Advanced statistical calculations including profit factors, win rates, and detailed breakdowns

### Docker Integration
- **Container Monitoring**: Direct Docker API integration to monitor three specific containers (Yuva_Positions_trading_bot, Shan_Positions_trading_bot, log-reader)
- **Log Processing**: Real-time parsing of trading bot logs to extract position data and trading signals
- **Health Checks**: Automatic container status updates with uptime calculations

### Enhanced Trading Analytics Engine
- **Advanced Multi-user Statistics**: Detailed separate tracking with period-based comparisons for Yuva and Shan
- **Real-time Position Management**: Live tracking of LONG/SHORT positions with unrealized P&L calculations
- **Enhanced Performance Metrics**: Comprehensive metrics including success rates by position type, average wins/losses, and profit factors
- **Period-based Analysis**: Time-filtered analytics (today, week, month, year, all-time) for performance tracking
- **Interactive Visualizations**: Professional charts for performance comparison and trading distribution analysis

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web framework with SQLAlchemy database integration
- **Docker Python SDK**: Container monitoring and status checking
- **SQLAlchemy**: Database ORM with declarative base models

### Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive UI components
- **Font Awesome 6**: Icon library for dashboard visual elements
- **Chart.js**: JavaScript charting library for performance visualization

### Trading Platform Integration
- **Binance API**: Indirect integration through containerized trading bots for position and order data
- **Log File Monitoring**: File-based log parsing from trading bot containers

### Production Infrastructure
- **PostgreSQL**: Production database with connection pooling and performance optimization
- **Docker Engine**: Container runtime for trading bot management and log processing
- **Gunicorn WSGI Server**: Multi-worker production server configuration on port 24242
- **Ubuntu Server Deployment**: Optimized for Ubuntu server environment with systemd integration
- **ProxyFix Middleware**: Production deployment support with reverse proxy handling
- **Enhanced Log Processing**: Advanced log parsing from trading bot containers with real-time updates
# Enhanced Trading Dashboard

## Overview

This is a comprehensive real-time trading dashboard built with Flask that monitors Docker containers running Binance trading bots for two users (Yuva and Shan). The enhanced system includes advanced trade history storage, period-based analytics (daily, weekly, monthly, yearly), professional UI design, and runs on port 24242 for Ubuntu server deployment. The dashboard provides detailed performance comparisons, interactive charts, comprehensive trade filtering, and real-time P&L calculations with PostgreSQL database storage.

## User Preferences

Preferred communication style: Simple, everyday language.
Preferred deployment: Replit environment on port 5000 (migrated from Ubuntu server deployment)
Migration status: Successfully migrated from Replit Agent to Replit environment with PostgreSQL database
Design preference: Clean, professional Phoenix-style light theme dashboard focusing exclusively on Long vs Short comparison
Data requirements: Complete trade history storage with period-based comparisons (today, yesterday, week, month, year, all-time)
Analytics focus: Long vs Short position performance analysis with historical trends

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
- **Historical Analytics Service**: Comprehensive trade history analysis with Long vs Short comparisons
- **Period-based Comparisons**: Complete analytics for today, yesterday, week, month, year, and all-time periods
- **Real-time Position Management**: Live tracking of LONG/SHORT positions with unrealized P&L calculations
- **Performance Metrics**: Success rates, profit factors, win rates, and trend analysis by position type
- **Weekly/Monthly Trends**: Historical comparison charts showing Long vs Short performance over time
- **Automated Data Storage**: Daily statistics saved automatically for long-term trend analysis
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
- **PostgreSQL**: Production database with comprehensive trade history storage and indexing
- **Docker Engine**: Container runtime for trading bot management and log processing
- **Gunicorn WSGI Server**: Multi-worker production server configuration on port 24242 ONLY
- **Ubuntu Server Deployment**: Complete systemd service integration with automated setup scripts
- **ProxyFix Middleware**: Production deployment support with reverse proxy handling
- **Enhanced Log Processing**: Advanced log parsing from trading bot containers with real-time updates
- **Automated Service Management**: Quick start scripts and service configuration for easy deployment
- **Historical Data Pipeline**: Automated daily statistics collection and trend analysis
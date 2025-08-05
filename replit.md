# Trading Dashboard

## Overview

This is a real-time trading dashboard built with Flask that monitors Docker containers running Binance trading bots for two users (Yuva and Shan). The system tracks trading positions, analyzes performance metrics, parses container logs, and provides a comprehensive web interface for monitoring trading activities. The dashboard displays container health status, trading statistics, profit/loss calculations, and real-time position data.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Flask Web Framework**: Core web application using Flask with SQLAlchemy ORM for database operations
- **Modular Service Layer**: Separate services for Docker monitoring, log parsing, and trading analytics
- **Database Models**: SQLAlchemy models for trading sessions, container status, and trading statistics
- **RESTful API**: JSON endpoints for real-time data updates and frontend integration

### Frontend Architecture
- **Bootstrap 5 UI**: Modern responsive design with dark theme optimized for trading environments
- **Real-time Updates**: JavaScript-based auto-refresh functionality with 30-second intervals
- **Interactive Charts**: Chart.js integration for visualizing trading performance and metrics
- **Component-based Templates**: Jinja2 templating with base template inheritance

### Data Storage
- **SQLite Database**: Local database storage with automatic table creation via SQLAlchemy migrations
- **Trading Session Tracking**: Comprehensive position tracking including entry/exit prices, PnL, and status
- **Container Monitoring**: Real-time Docker container status and uptime tracking
- **Performance Analytics**: Statistical calculations for win rates, profit factors, and trade analysis

### Docker Integration
- **Container Monitoring**: Direct Docker API integration to monitor three specific containers (Yuva_Positions_trading_bot, Shan_Positions_trading_bot, log-reader)
- **Log Processing**: Real-time parsing of trading bot logs to extract position data and trading signals
- **Health Checks**: Automatic container status updates with uptime calculations

### Trading Analytics Engine
- **Multi-user Statistics**: Separate tracking and analysis for Yuva and Shan trading accounts
- **Position Management**: Real-time tracking of LONG/SHORT positions across multiple cryptocurrency symbols
- **Performance Metrics**: Comprehensive calculations including win rates, profit factors, and average profit/loss ratios
- **Risk Analysis**: Position sizing and PnL tracking for risk management insights

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

### Infrastructure
- **SQLite**: Local database for development with PostgreSQL readiness
- **Docker Engine**: Container runtime for trading bot management
- **ProxyFix Middleware**: Production deployment support with reverse proxy handling
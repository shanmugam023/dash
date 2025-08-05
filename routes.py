from flask import render_template, jsonify, request
from app import app, db
from models import TradingSession, ContainerStatus, TradingStats
from services.docker_monitor import DockerMonitor
from services.enhanced_log_parser import EnhancedLogParser
from services.trading_analytics import TradingAnalytics
from services.historical_analytics import historical_analytics
from services.log_reader_service import LogReaderService
from services.trading_status_service import TradingStatusService
import logging

# Initialize services
docker_monitor = DockerMonitor()
log_parser = EnhancedLogParser()
trading_analytics = TradingAnalytics()
log_reader_service = LogReaderService()
trading_status_service = TradingStatusService()

@app.route('/')
def dashboard():
    """Enhanced dashboard route"""
    try:
        # Get container statuses
        containers = docker_monitor.get_container_status()
        
        # Get trading statistics
        yuva_stats = trading_analytics.get_user_stats('Yuva')
        shan_stats = trading_analytics.get_user_stats('Shan')
        
        # Get recent trading sessions (increased limit)
        recent_trades = TradingSession.query.order_by(TradingSession.created_at.desc()).limit(50).all()
        
        # Get current positions
        current_positions = trading_analytics.get_current_positions()
        
        # Parse latest logs for real-time data
        log_parser.parse_latest_logs()
        
        # Get trading summary from log-reader
        trading_summary = log_reader_service.get_trading_summary()
        
        # Get real-time trading status
        trading_status = trading_status_service.get_current_status()
        mode_indicator = trading_status_service.get_mode_indicator()
        container_status = trading_status_service.get_container_status_summary()
        trading_counts = trading_status_service.get_trading_counts()
        
        return render_template('modern_dashboard.html',
                             containers=containers,
                             yuva_stats=yuva_stats,
                             shan_stats=shan_stats,
                             recent_trades=recent_trades,
                             current_positions=current_positions,
                             trading_summary=trading_summary,
                             trading_status=trading_status,
                             mode_indicator=mode_indicator,
                             container_status=container_status,
                             trading_counts=trading_counts)
    except Exception as e:
        logging.error(f"Dashboard error: {e}")
        # Get default trading status even on error
        trading_status = trading_status_service.get_current_status()
        mode_indicator = trading_status_service.get_mode_indicator()
        container_status = trading_status_service.get_container_status_summary()
        trading_counts = trading_status_service.get_trading_counts()
        
        return render_template('modern_dashboard.html',
                             containers=[],
                             yuva_stats={},
                             shan_stats={},
                             recent_trades=[],
                             current_positions=[],
                             trading_summary={},
                             trading_status=trading_status,
                             mode_indicator=mode_indicator,
                             container_status=container_status,
                             trading_counts=trading_counts)

@app.route('/api/container-status')
def api_container_status():
    """API endpoint for container status"""
    try:
        containers = docker_monitor.get_container_status()
        return jsonify(containers)
    except Exception as e:
        logging.error(f"Container status API error: {e}")
        return jsonify([])

@app.route('/api/trading-stats')
def api_trading_stats():
    """API endpoint for trading statistics"""
    try:
        yuva_stats = trading_analytics.get_user_stats('Yuva')
        shan_stats = trading_analytics.get_user_stats('Shan')
        
        return jsonify({
            'yuva': yuva_stats,
            'shan': shan_stats
        })
    except Exception as e:
        logging.error(f"Trading stats API error: {e}")
        return jsonify({'yuva': {}, 'shan': {}})

@app.route('/api/logs')
def api_logs():
    """API endpoint for recent logs"""
    try:
        logs = log_parser.get_recent_logs(limit=50)
        return jsonify(logs)
    except Exception as e:
        logging.error(f"Logs API error: {e}")
        return jsonify([])

@app.route('/api/trade-history/<period>')
def api_trade_history(period):
    """API endpoint for trade history by period"""
    try:
        trades = trading_analytics.get_trade_history_by_period(period)
        return jsonify(trades)
    except Exception as e:
        logging.error(f"Trade history API error: {e}")
        return jsonify([])

@app.route('/api/statistics/<user>/<period>')
def api_user_statistics(user, period):
    """API endpoint for user statistics by period"""
    try:
        stats = trading_analytics.get_user_stats_by_period(user, period)
        return jsonify(stats)
    except Exception as e:
        logging.error(f"User statistics API error: {e}")
        return jsonify({})

@app.route('/api/refresh-data')
def api_refresh_data():
    """Refresh all data"""
    try:
        # Update container statuses
        docker_monitor.update_container_status()
        
        # Parse latest logs
        log_parser.parse_latest_logs()
        
        # Recalculate analytics
        trading_analytics.update_statistics()
        
        return jsonify({'status': 'success'})
    except Exception as e:
        logging.error(f"Refresh data error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/log-reader')
def api_log_reader():
    """API endpoint for log-reader container logs"""
    try:
        lines = request.args.get('lines', 100, type=int)
        logs = log_reader_service.get_log_reader_logs(lines=lines)
        return jsonify(logs)
    except Exception as e:
        logging.error(f"Log reader API error: {e}")
        return jsonify([])

@app.route('/api/trading-summary')
def api_trading_summary():
    """API endpoint for trading summary from log-reader"""
    try:
        summary = log_reader_service.get_trading_summary()
        return jsonify(summary)
    except Exception as e:
        logging.error(f"Trading summary API error: {e}")
        return jsonify({})

@app.route('/logs')
def logs_viewer():
    """Dedicated logs viewer page"""
    try:
        # Get log reader logs
        logs = log_reader_service.get_log_reader_logs(lines=200)
        trading_summary = log_reader_service.get_trading_summary()
        
        return render_template('logs_viewer.html',
                             logs=logs,
                             trading_summary=trading_summary)
    except Exception as e:
        logging.error(f"Logs viewer error: {e}")
        return render_template('logs_viewer.html',
                             logs=[],
                             trading_summary={})

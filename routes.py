from flask import render_template, jsonify, request
from app import app, db
from models import TradingSession, ContainerStatus, TradingStats
from services.docker_monitor import DockerMonitor
from services.log_parser import LogParser
from services.trading_analytics import TradingAnalytics
import logging

# Initialize services
docker_monitor = DockerMonitor()
log_parser = LogParser()
trading_analytics = TradingAnalytics()

@app.route('/')
def dashboard():
    """Main dashboard route"""
    try:
        # Get container statuses
        containers = docker_monitor.get_container_status()
        
        # Get trading statistics
        yuva_stats = trading_analytics.get_user_stats('Yuva')
        shan_stats = trading_analytics.get_user_stats('Shan')
        
        # Get recent trading sessions
        recent_trades = TradingSession.query.order_by(TradingSession.created_at.desc()).limit(10).all()
        
        # Get current positions
        current_positions = trading_analytics.get_current_positions()
        
        return render_template('dashboard.html',
                             containers=containers,
                             yuva_stats=yuva_stats,
                             shan_stats=shan_stats,
                             recent_trades=recent_trades,
                             current_positions=current_positions)
    except Exception as e:
        logging.error(f"Dashboard error: {e}")
        return render_template('dashboard.html',
                             containers=[],
                             yuva_stats={},
                             shan_stats={},
                             recent_trades=[],
                             current_positions=[])

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

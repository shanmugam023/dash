from app import db
from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, Boolean, Text, Index, JSON

class TradingSession(db.Model):
    id = db.Column(Integer, primary_key=True)
    user = db.Column(String(50), nullable=False)  # 'Yuva' or 'Shan'
    symbol = db.Column(String(20), nullable=False)
    side = db.Column(String(10), nullable=False)  # 'LONG' or 'SHORT'
    entry_price = db.Column(Float, nullable=False)
    exit_price = db.Column(Float)
    position_size = db.Column(Float, nullable=False)
    pnl = db.Column(Float, default=0.0)
    realized_pnl = db.Column(Float, default=0.0)
    unrealized_pnl = db.Column(Float, default=0.0)
    status = db.Column(String(20), default='OPEN')  # 'OPEN', 'CLOSED', 'STOPPED'
    trade_type = db.Column(String(20), default='MANUAL')  # 'MANUAL', 'AUTO', 'STOP_LOSS', 'TAKE_PROFIT'
    strategy = db.Column(String(100))
    notes = db.Column(Text)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    closed_at = db.Column(DateTime)
    
    # Add indexes for better query performance
    __table_args__ = (
        Index('idx_user_created', 'user', 'created_at'),
        Index('idx_symbol_status', 'symbol', 'status'),
        Index('idx_user_side', 'user', 'side'),
    )

class ContainerStatus(db.Model):
    id = db.Column(Integer, primary_key=True)
    container_name = db.Column(String(100), nullable=False, unique=True)
    status = db.Column(String(20), nullable=False)
    last_updated = db.Column(DateTime, default=datetime.utcnow)
    uptime = db.Column(String(50))

class TradingStats(db.Model):
    id = db.Column(Integer, primary_key=True)
    user = db.Column(String(50), nullable=False)
    period = db.Column(String(20), nullable=False)  # 'daily', 'weekly', 'monthly', 'yearly'
    period_date = db.Column(DateTime, nullable=False)  # Start date of the period
    total_trades = db.Column(Integer, default=0)
    successful_trades = db.Column(Integer, default=0)
    failed_trades = db.Column(Integer, default=0)
    long_trades = db.Column(Integer, default=0)
    short_trades = db.Column(Integer, default=0)
    long_successful = db.Column(Integer, default=0)
    long_failed = db.Column(Integer, default=0)
    short_successful = db.Column(Integer, default=0)
    short_failed = db.Column(Integer, default=0)
    total_pnl = db.Column(Float, default=0.0)
    total_volume = db.Column(Float, default=0.0)
    win_rate = db.Column(Float, default=0.0)
    profit_factor = db.Column(Float, default=0.0)
    avg_win = db.Column(Float, default=0.0)
    avg_loss = db.Column(Float, default=0.0)
    max_drawdown = db.Column(Float, default=0.0)
    last_updated = db.Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_user_period', 'user', 'period', 'period_date'),
    )

class LogReaderData(db.Model):
    """Store historical data from log-reader container"""
    id = db.Column(Integer, primary_key=True)
    timestamp = db.Column(DateTime, nullable=False, default=datetime.utcnow)
    log_type = db.Column(String(50))  # 'status_update', 'system_alert', etc.
    message = db.Column(Text)
    raw_data = db.Column(JSON)  # Store structured log data
    buy_container_running = db.Column(Boolean, default=False)
    sell_container_running = db.Column(Boolean, default=False)
    api_calls_enabled = db.Column(Boolean, default=False)
    buy_success_count = db.Column(Integer, default=0)
    buy_stop_loss_count = db.Column(Integer, default=0)
    sell_success_count = db.Column(Integer, default=0)
    sell_stop_loss_count = db.Column(Integer, default=0)
    live_trade_success_count = db.Column(Integer, default=0)
    live_trade_failure_count = db.Column(Integer, default=0)
    buy_coins_tracking = db.Column(Integer, default=0)
    sell_coins_tracking = db.Column(Integer, default=0)
    
    __table_args__ = (
        Index('idx_timestamp', 'timestamp'),
        Index('idx_log_type', 'log_type'),
    )

class DailyLogSummary(db.Model):
    """Daily aggregated summary from log-reader data"""
    id = db.Column(Integer, primary_key=True)
    date = db.Column(DateTime, nullable=False)  # Date without time
    total_buy_success = db.Column(Integer, default=0)
    total_buy_failures = db.Column(Integer, default=0)
    total_sell_success = db.Column(Integer, default=0)
    total_sell_failures = db.Column(Integer, default=0)
    total_live_trades_success = db.Column(Integer, default=0)
    total_live_trades_failure = db.Column(Integer, default=0)
    avg_buy_coins_tracking = db.Column(Float, default=0.0)
    avg_sell_coins_tracking = db.Column(Float, default=0.0)
    api_enabled_duration = db.Column(Float, default=0.0)  # Hours API was enabled
    buy_container_uptime = db.Column(Float, default=0.0)  # Hours container was running
    sell_container_uptime = db.Column(Float, default=0.0)  # Hours container was running
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_date', 'date'),
    )

class WeeklyLogSummary(db.Model):
    """Weekly aggregated summary"""
    id = db.Column(Integer, primary_key=True)
    week_start = db.Column(DateTime, nullable=False)
    week_end = db.Column(DateTime, nullable=False)
    total_buy_success = db.Column(Integer, default=0)
    total_buy_failures = db.Column(Integer, default=0)
    total_sell_success = db.Column(Integer, default=0)
    total_sell_failures = db.Column(Integer, default=0)
    total_live_trades_success = db.Column(Integer, default=0)
    total_live_trades_failure = db.Column(Integer, default=0)
    avg_daily_buy_coins = db.Column(Float, default=0.0)
    avg_daily_sell_coins = db.Column(Float, default=0.0)
    success_rate = db.Column(Float, default=0.0)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_week_start', 'week_start'),
    )

class MonthlyLogSummary(db.Model):
    """Monthly aggregated summary"""
    id = db.Column(Integer, primary_key=True)
    month = db.Column(Integer, nullable=False)  # 1-12
    year = db.Column(Integer, nullable=False)
    total_buy_success = db.Column(Integer, default=0)
    total_buy_failures = db.Column(Integer, default=0)
    total_sell_success = db.Column(Integer, default=0)
    total_sell_failures = db.Column(Integer, default=0)
    total_live_trades_success = db.Column(Integer, default=0)
    total_live_trades_failure = db.Column(Integer, default=0)
    avg_daily_volume = db.Column(Float, default=0.0)
    success_rate = db.Column(Float, default=0.0)
    best_day = db.Column(DateTime)
    worst_day = db.Column(DateTime)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_year_month', 'year', 'month'),
    )

from app import db
from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, Boolean, Text, Index

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

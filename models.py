from app import db
from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, Boolean, Text

class TradingSession(db.Model):
    id = db.Column(Integer, primary_key=True)
    user = db.Column(String(50), nullable=False)  # 'Yuva' or 'Shan'
    symbol = db.Column(String(20), nullable=False)
    side = db.Column(String(10), nullable=False)  # 'LONG' or 'SHORT'
    entry_price = db.Column(Float, nullable=False)
    exit_price = db.Column(Float)
    position_size = db.Column(Float, nullable=False)
    pnl = db.Column(Float, default=0.0)
    status = db.Column(String(20), default='OPEN')  # 'OPEN', 'CLOSED', 'STOPPED'
    created_at = db.Column(DateTime, default=datetime.utcnow)
    closed_at = db.Column(DateTime)

class ContainerStatus(db.Model):
    id = db.Column(Integer, primary_key=True)
    container_name = db.Column(String(100), nullable=False, unique=True)
    status = db.Column(String(20), nullable=False)
    last_updated = db.Column(DateTime, default=datetime.utcnow)
    uptime = db.Column(String(50))

class TradingStats(db.Model):
    id = db.Column(Integer, primary_key=True)
    user = db.Column(String(50), nullable=False)
    total_trades = db.Column(Integer, default=0)
    successful_trades = db.Column(Integer, default=0)
    failed_trades = db.Column(Integer, default=0)
    long_trades = db.Column(Integer, default=0)
    short_trades = db.Column(Integer, default=0)
    total_pnl = db.Column(Float, default=0.0)
    win_rate = db.Column(Float, default=0.0)
    last_updated = db.Column(DateTime, default=datetime.utcnow)

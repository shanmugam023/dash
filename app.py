import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "trading_dashboard_secret_key_replit_2025")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure database based on environment
database_url = os.environ.get("DATABASE_URL")
if database_url:
    # Replit environment with PostgreSQL
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    # Ubuntu deployment with SQLite
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trading_dashboard.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models to ensure tables are created
    import models
    db.create_all()
    
    # Initialize live trading simulator
    try:
        from services.live_trading_simulator import live_simulator
        live_simulator.initialize_current_positions()
    except Exception as e:
        logging.error(f"Error initializing trading simulator: {e}")

# Import routes
from routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

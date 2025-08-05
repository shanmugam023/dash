# Trading Dashboard Deployment Instructions

## Quick Setup for Your System

### Option 1: Automated Setup (Recommended)

```bash
# Download the project files to your server
# Then run the quick start script:
chmod +x quick_start.sh
./quick_start.sh
```

This will automatically:
- Create virtual environment
- Install dependencies  
- Create configuration files
- Give you options to run development, production, or setup as service

### Option 2: Manual Setup

### Prerequisites
- Python 3.8+ installed
- Git installed
- PostgreSQL database (or use the provided PostgreSQL setup)

### Step 1: Download and Setup

```bash
# Clone the repository
git clone <your-repository-url>
cd trading-dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install flask flask-sqlalchemy gunicorn psycopg2-binary python-dotenv docker werkzeug
```

### Step 2: Database Setup

#### Option A: Use PostgreSQL (Recommended)
```bash
# Install PostgreSQL if not installed
sudo apt update
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE trading_dashboard;
CREATE USER trading_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE trading_dashboard TO trading_user;
\q
```

#### Option B: Use Environment Database (Automatic)
The app will automatically create the database tables when you run it.

### Step 3: Environment Configuration

Create a `.env` file in the project root:

```bash
DATABASE_URL=postgresql://trading_user:your_password@localhost/trading_dashboard
SESSION_SECRET=your_secret_key_here_make_it_long_and_random
FLASK_ENV=production
```

### Step 4: Run the Application

#### Development Mode (Port 5000)
```bash
python main.py
```

#### Production Mode (Port 5000 - Default)
```bash
python start_server.py
```

#### Production Mode (Port 24242 - Ubuntu Server)
Edit `gunicorn_config.py` and change:
```python
bind = "0.0.0.0:24242"
```

Then edit `start_server.py` and change all port references from 5000 to 24242.

Then run:
```bash
python start_server.py
```

### Step 5: Access Your Dashboard

Open your web browser and go to:
- Development: `http://localhost:5000`
- Production: `http://localhost:5000` (or `http://localhost:24242` if configured)
- Server: `http://your-server-ip:24242`

## Features You'll See

### Dashboard Overview
✓ **Clean Phoenix-style Design** - Professional ecommerce-inspired interface
✓ **Long vs Short Performance** - Focus on position types rather than users
✓ **Real-time Trading Data** - Live P&L calculations and position tracking
✓ **Interactive Charts** - Performance visualization with Chart.js
✓ **Current Positions Table** - Active trades with real-time updates

### Trading Analytics
✓ **Period-based Filtering** - View data by Today, Week, Month, Year
✓ **Performance Metrics** - Success rates, profit factors, win rates
✓ **Position Breakdown** - Separate tracking for LONG and SHORT positions
✓ **Bot Status Monitoring** - Trading bot health and activity status

### Data Processing
✓ **Automatic Log Parsing** - Processes your AVAUSDT and other trading logs
✓ **Database Storage** - Complete trade history with PostgreSQL
✓ **Real-time Updates** - Dashboard refreshes automatically

## Ubuntu Server Deployment

### For Port 24242 (Your Preference)

1. **Install System Dependencies**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib nginx
```

2. **Setup Application**
```bash
git clone <your-repo>
cd trading-dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Configure for Port 24242**
```bash
# Edit gunicorn_config.py
nano gunicorn_config.py
# Change: bind = "0.0.0.0:24242"

# Edit start_server.py port references
nano start_server.py
# Change all 5000 references to 24242
```

4. **Setup as System Service (Automated)**
```bash
chmod +x setup_service.sh
./setup_service.sh
```

This will automatically:
- Create the systemd service file
- Configure environment variables
- Enable the service
- Provide management commands

5. **Manual Service Management**
```bash
# Start the service
sudo systemctl start trading-dashboard

# Check status
sudo systemctl status trading-dashboard

# View logs
sudo journalctl -u trading-dashboard -f

# Stop the service
sudo systemctl stop trading-dashboard

# Restart the service  
sudo systemctl restart trading-dashboard
```

6. **Configure Firewall**
```bash
sudo ufw allow 24242
sudo ufw reload
```

### Access Your Dashboard
Your dashboard will be available at: `http://your-server-ip:24242`

## Troubleshooting

### Common Issues

1. **Port Already in Use**
```bash
sudo lsof -i :24242
sudo kill -9 <PID>
```

2. **Database Connection Error**
- Check DATABASE_URL in .env file
- Ensure PostgreSQL is running: `sudo systemctl status postgresql`
- Test connection: `psql $DATABASE_URL`

3. **Python Dependencies Missing**
```bash
pip install -r requirements.txt
```

4. **Permission Denied**
```bash
chmod +x start_server.py
```

### Logs and Monitoring
```bash
# View application logs
journalctl -u trading-dashboard -f

# Check system resources
htop

# Monitor network connections
netstat -tulpn | grep :24242
```

## Configuration Options

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `SESSION_SECRET`: Secret key for sessions
- `FLASK_ENV`: development or production
- `FLASK_DEBUG`: 1 for debug mode

### Customization
- **Port**: Edit `gunicorn_config.py` and `start_server.py`
- **Workers**: Edit `gunicorn_config.py` workers setting
- **Styling**: Modify `static/css/phoenix_dashboard.css`
- **Features**: Update templates in `templates/` directory

## Support

If you encounter any issues:
1. Check the logs: `journalctl -u trading-dashboard -f`
2. Verify all dependencies are installed
3. Ensure PostgreSQL is running and accessible
4. Check firewall settings for your chosen port

Your trading dashboard is now ready with a professional Phoenix-style interface focusing on Long vs Short performance analysis!
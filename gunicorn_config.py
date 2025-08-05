# Gunicorn configuration file for trading dashboard
import os

# Server socket
bind = "0.0.0.0:24242"
backlog = 2048

# Worker processes
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100

# Restart workers after this many requests, with up to 100 random seconds
# This helps prevent memory leaks
preload_app = True

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "trading_dashboard"

# Development vs Production
debug = os.getenv("FLASK_ENV") == "development"
reload = debug

def when_ready(server):
    server.log.info("Trading Dashboard is ready to serve requests on port 24242")

def worker_int(worker):
    worker.log.info("Worker received INT or QUIT signal")

def pre_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)
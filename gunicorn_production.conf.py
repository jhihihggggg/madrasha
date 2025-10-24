# Gunicorn Production Configuration for Madrasha Ummul Qura
# File: gunicorn_production.conf.py

import os
import multiprocessing

# Server socket
bind = "127.0.0.1:8000"  # Bind to localhost (Nginx will proxy)
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"  # Use gevent for better concurrency
worker_connections = 1000
timeout = 120  # Increase timeout for database operations
keepalive = 5

# Restart workers to prevent memory leaks
max_requests = 1000
max_requests_jitter = 100

# Logging
errorlog = "/var/www/madrasha/logs/gunicorn_error.log"
loglevel = "info"
accesslog = "/var/www/madrasha/logs/gunicorn_access.log"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'madrasha-app'

# Server mechanics
daemon = False
pidfile = "/tmp/madrasha.pid"
umask = 0
user = None  # Set by systemd service
group = None  # Set by systemd service

# Preload application for better performance
preload_app = True

# Server hooks for better monitoring
def on_starting(server):
    """Called just before the master process is initialized."""
    server.log.info("🕌 Starting Madrasha Ummul Qura server...")

def on_reload(server):
    """Called to recycle workers during a reload via SIGHUP."""
    server.log.info("♻️  Reloading Madrasha server...")

def when_ready(server):
    """Called just after the server is started."""
    server.log.info("✓ Madrasha server is ready. Accepting connections.")

def pre_fork(server, worker):
    """Called just before a worker is forked."""
    pass

def post_fork(server, worker):
    """Called just after a worker has been forked."""
    server.log.info(f"Worker spawned (pid: {worker.pid})")

def pre_exec(server):
    """Called just before a new master process is forked."""
    server.log.info("Forked child, re-executing.")

def worker_int(worker):
    """Called just after a worker exited on SIGINT or SIGQUIT."""
    worker.log.info("Worker received INT or QUIT signal")

def worker_abort(worker):
    """Called when a worker received the SIGABRT signal."""
    worker.log.info("Worker received SIGABRT signal")

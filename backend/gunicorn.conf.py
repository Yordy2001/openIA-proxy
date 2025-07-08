#!/usr/bin/env python3
"""
Configuración de Gunicorn para producción
"""

import multiprocessing
import os

# Configuración básica
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
preload_app = True
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Timeouts
timeout = 120
graceful_timeout = 30

# SSL (si se usa)
# keyfile = "/path/to/key.pem"
# certfile = "/path/to/cert.pem"

# Configuración avanzada
forwarded_allow_ips = "*"
proxy_allow_ips = "*"
proxy_protocol = False

# Restart workers
max_requests = 1000
max_requests_jitter = 50

# Daemon mode (para systemd)
daemon = False
pidfile = "/tmp/gunicorn.pid"

# Capturar señales
capture_output = True
enable_stdio_inheritance = True

def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")

def pre_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_worker_init(worker):
    worker.log.info("Worker initialized (pid: %s)", worker.pid)

def worker_abort(worker):
    worker.log.info("Worker aborted (pid: %s)", worker.pid) 
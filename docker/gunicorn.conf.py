import os

bind = "0.0.0.0:5000"
timeout = 60
workers = os.environ.get('GUNICORN_WORKERS', 2)
worker_class = "uvicorn.workers.UvicornWorker"

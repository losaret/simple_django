# gunicorn.conf.py
import os

# Базовая директория
base_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(base_dir, 'logs')
os.makedirs(log_dir, exist_ok=True)

bind = "0.0.0.0:8000"
workers = 3
worker_class = "sync"

# Логирование
loglevel = "info"
accesslog = os.path.join(log_dir, "gunicorn_access.log")
errorlog = os.path.join(log_dir, "gunicorn_error.log")
capture_output = True
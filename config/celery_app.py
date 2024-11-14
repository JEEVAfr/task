# celery.py

import os
from celery import Celery
from celery.schedules import crontab
from django.utils.module_loading import import_string

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("apps")
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Register class-based tasks (if any)
for _import_string in []:
    app.register_task(import_string(_import_string)())

# Ensure Celery retries connection to Redis (if using Redis as broker)
app.conf.broker_connection_retry_on_startup = True


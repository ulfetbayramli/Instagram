from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Instagram.settings')
from celery.schedules import crontab

app = Celery('Instagram')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update_instagram_stats': {
        'task': 'users.tasks.update_instagram_stats',
        'schedule': timedelta(minutes=3),
    },
}

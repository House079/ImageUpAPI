import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest_img.settings')
app = Celery('rest_img')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('default')
app.config_from_object('django.conf:settings', namespace='CELERY_DEFAULT')
app.autodiscover_tasks(['project.apps.video_archive'])


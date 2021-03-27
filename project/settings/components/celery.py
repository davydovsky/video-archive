import datetime

from project.settings.components import config

# Celery settings.
RABBITMQ_HOST = config('RABBITMQ_HOST')
RABBITMQ_LOGIN = config('RABBITMQ_LOGIN')
RABBITMQ_PASSWORD = config('RABBITMQ_PASSWORD')
RABBITMQ_PORT = config('RABBITMQ_PORT', cast=int, default=5672)

CELERY_DEFAULT_BROKER_URL = f'amqp://{RABBITMQ_LOGIN}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/video-archive'
CELERY_DEFAULT_RESULT_BACKEND = 'django-db'
CELERY_DEFAULT_RESULT_EXPIRES = datetime.timedelta(days=10)
SOFT_TIME_LIMIT = config('SOFT_TIME_LIMIT', cast=int, default=86400)

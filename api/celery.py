from celery import Celery

from api.config import Config

celery = Celery(
    'celery',
    broker=f'redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}',
    include=['app.celery_tasks']
)

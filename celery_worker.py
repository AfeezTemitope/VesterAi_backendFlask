from celery import Celery
from config import Config

app = Celery('tasks', broker=Config.REDIS_URL)


app.conf.update(
    result_backend=Config.REDIS_URL,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

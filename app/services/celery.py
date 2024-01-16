from celery import Celery
from app.core.config import settings


def make_celery(app_name=__name__):
    return Celery(app_name, broker=settings.BROKER_URL)


celery = make_celery()
celery.autodiscover_tasks(['app.utils']) 
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meinberlin.config.settings")

celery_app = Celery()
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()


@celery_app.task(name="dummy_task")
def dummy_task():
    """
    This task is for testing purposes only.
    """

    result = "hello world"
    print(result)

    return result


@celery_app.task(name="crash_task")
def crash_task():
    """
    This task is for testing purposes only.
    """

    1 / 0

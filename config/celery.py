import os

from celery import Celery


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

app = Celery("config")

app.config_from_object(
    "django.conf:settings",
    namespace="CELERY"
)

app.autodiscover_tasks()

from celery.schedules import crontab

app.conf.beat_schedule = {
    "deactivate-expired-urls-every-10-minutes": {
        "task": "shortener.tasks.deactivate_expired_urls",
        "schedule": crontab(minute="*/10"),
    },
}
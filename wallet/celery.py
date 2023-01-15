import os

from celery import Celery

from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wallet.settings")

app = Celery("wallet")

CELERY_BEAT_SCHEDULE = {
    "send_cashback_info": {
        "task": "wallet.cashback.tasks.send_cashback_info",
        "schedule": crontab(minute="*/1"),
    },
}
app.conf.beat_schedule = CELERY_BEAT_SCHEDULE

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

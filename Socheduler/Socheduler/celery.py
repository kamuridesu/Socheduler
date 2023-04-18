import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTING_MODULE", "Socheduler.settings")
app = Celery("Socheduler")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
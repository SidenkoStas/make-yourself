from celery import Celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'make_yourself.settings')

app = Celery("make_yourself")

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

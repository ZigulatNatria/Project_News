import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('newspaper')
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'mailing_monday_8': {
        'task': 'news.tasks.mailing_monday',
        # 'schedule': crontab(),
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': None,
    },
}


app.autodiscover_tasks()
import os
from celery.schedules import crontab
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WOWito.settings')

app = Celery('WOWito')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'clear_board_every_minute': {
        'task': 'board.tasks.send_news',
        'schedule': crontab(minute='12', hour='12', day_of_week='monday'),
    }
}

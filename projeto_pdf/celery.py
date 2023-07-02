from __future__ import absolute_import, unicode_literals

import logging
import os

from celery import Celery
from celery.schedules import crontab
from celery.signals import after_setup_logger

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_pdf.settings')

app = Celery('projeto_pdf')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-5-minutes': {
        'task': 'notas.tasks.task_atualizar_notas',
        'schedule': crontab(minute=0),
    },
    # Aqui você pode adicionar mais tarefas periódicas conforme necessário Parar se atualizar de 5 minutos:  'schedule': crontab(minute='*/5'),
}











@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler('/home/ubuntu/sistemas/celery.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
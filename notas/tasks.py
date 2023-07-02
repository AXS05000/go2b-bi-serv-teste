from celery import shared_task

from .views import atualizar_notas_automaticamente


@shared_task
def task_atualizar_notas():
    atualizar_notas_automaticamente()
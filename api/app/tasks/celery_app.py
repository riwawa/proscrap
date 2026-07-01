from celery import Celery
from celery.schedules import crontab

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "datajud_monitor",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.tasks.consulta_processos"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Celery Beat: todo dia às 06:00 UTC (03:00 BRT / 08:00 BRST)
celery_app.conf.beat_schedule = {
    "consulta-diaria-processos": {
        "task": "app.tasks.consulta_processos.consultar_todos_processos_ativos",
        "schedule": crontab(hour=settings.consulta_diaria_hora_utc, minute=0),
    },
}
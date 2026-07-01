"""
Tasks Celery de consulta à API DataJud.

S3: implementação real das tasks (substitui os placeholders NotImplementedError do setup inicial).
"""
import logging

from celery import group

from app.core.database import SessionLocal
from app.models.processo import Processo
from app.services.sincronizacao import sincronizar_processo
from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(
    name="app.tasks.consulta_processos.consultar_todos_processos_ativos",
    bind=True,
    max_retries=0,
)
def consultar_todos_processos_ativos(self):
    """
    Dispara uma task individual para cada processo ativo cadastrado.
    Chamada pelo Celery Beat diariamente (ver celery_app.py beat_schedule).
    """
    db = SessionLocal()
    try:
        processos = db.query(Processo).filter(Processo.ativo == True).all()
        ids = [str(p.id) for p in processos]
        logger.info(f"Agendando consulta para {len(ids)} processo(s) ativo(s).")
    finally:
        db.close()

    if ids:
        job = group(consultar_processo_individual.s(pid) for pid in ids)
        job.apply_async()

    return {"processos_agendados": len(ids)}


@celery_app.task(
    name="app.tasks.consulta_processos.consultar_processo_individual",
    bind=True,
    max_retries=3,
    default_retry_delay=60,  # 1 min entre retries
    time_limit=120,
    soft_time_limit=110,
)
def consultar_processo_individual(self, processo_id: str):
    """
    Consulta um processo específico, faz diff e persiste as movimentações novas.
    """
    db = SessionLocal()
    try:
        processo = db.query(Processo).filter(Processo.id == processo_id).first()
        if processo is None:
            logger.warning(f"Processo {processo_id} não encontrado, task ignorada.")
            return {"status": "not_found"}

        resultado = sincronizar_processo(processo, db)
        logger.info(
            f"Processo {processo_id}: status={resultado['status']} "
            f"novas={resultado['movimentacoes_novas']}"
        )
        return resultado

    except Exception as exc:
        logger.error(f"Erro ao consultar processo {processo_id}: {exc}")
        raise self.retry(exc=exc)
    finally:
        db.close()
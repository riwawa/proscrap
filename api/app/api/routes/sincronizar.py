import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.processo import Processo
from app.services.sincronizacao import sincronizar_processo

router = APIRouter(prefix="/processos", tags=["sincronizacao"])


@router.post("/{processo_id}/sincronizar")
def sincronizar(processo_id: uuid.UUID, db: Session = Depends(get_db)):
    processo = db.query(Processo).filter(Processo.id == processo_id).first()
    if processo is None:
        raise HTTPException(status_code=404, detail="Processo não encontrado.")
    if not processo.ativo:
        raise HTTPException(status_code=422, detail="Processo inativo.")

    resultado = sincronizar_processo(processo, db)

    if resultado["status"] == "error":
        raise HTTPException(status_code=502, detail=resultado["erro_detalhe"])

    return resultado
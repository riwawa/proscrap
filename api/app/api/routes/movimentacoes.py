import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.movimentacao import Movimentacao
from app.models.processo import Processo
from app.schemas.movimentacao import MovimentacaoRead

router = APIRouter(prefix="/processos/{processo_id}/movimentacoes", tags=["movimentacoes"])


@router.get("", response_model=list[MovimentacaoRead])
def listar_movimentacoes(processo_id: uuid.UUID, db: Session = Depends(get_db)):
    processo = db.query(Processo).filter(Processo.id == processo_id).first()
    if processo is None:
        raise HTTPException(status_code=404, detail="Processo não encontrado.")

    return (
        db.query(Movimentacao)
        .filter(Movimentacao.processo_id == processo_id)
        .order_by(Movimentacao.data_hora.desc())
        .all()
    )

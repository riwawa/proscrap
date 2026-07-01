import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.tribunal_endpoints import resolver_alias_por_numero_cnj
from app.models.processo import Processo
from app.schemas.processo import ProcessoCreate, ProcessoRead

router = APIRouter(prefix="/processos", tags=["processos"])


@router.post("", response_model=ProcessoRead, status_code=201)
def cadastrar_processo(payload: ProcessoCreate, db: Session = Depends(get_db)):
    alias = resolver_alias_por_numero_cnj(payload.numero_cnj)
    if alias is None:
        # Tabela J.TR -> alias ainda incompleta (pendência conhecida, ver core/tribunal_endpoints.py)
        raise HTTPException(
            status_code=422,
            detail=(
                "Não foi possível identificar o tribunal a partir do número informado. "
                "O mapeamento de tribunais ainda está sendo completado (ver TODO no S1)."
            ),
        )

    existente = db.query(Processo).filter(Processo.numero_cnj == payload.numero_cnj).first()
    if existente:
        raise HTTPException(status_code=409, detail="Processo já cadastrado.")

    processo = Processo(
        numero_cnj=payload.numero_cnj,
        tribunal_alias=alias,
        apelido=payload.apelido,
    )
    db.add(processo)
    db.commit()
    db.refresh(processo)
    return processo


@router.get("", response_model=list[ProcessoRead])
def listar_processos(db: Session = Depends(get_db)):
    return db.query(Processo).order_by(Processo.criado_em.desc()).all()


@router.get("/{processo_id}", response_model=ProcessoRead)
def obter_processo(processo_id: uuid.UUID, db: Session = Depends(get_db)):
    processo = db.query(Processo).filter(Processo.id == processo_id).first()
    if processo is None:
        raise HTTPException(status_code=404, detail="Processo não encontrado.")
    return processo


@router.delete("/{processo_id}", status_code=204)
def remover_processo(processo_id: uuid.UUID, db: Session = Depends(get_db)):
    processo = db.query(Processo).filter(Processo.id == processo_id).first()
    if processo is None:
        raise HTTPException(status_code=404, detail="Processo não encontrado.")
    db.delete(processo)
    db.commit()

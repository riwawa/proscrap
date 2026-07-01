import uuid

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Processo(Base):
    __tablename__ = "processos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_cnj = Column(String(25), nullable=False, unique=True, index=True)
    tribunal_alias = Column(String(50), nullable=False)
    apelido = Column(String(255), nullable=True)
    ativo = Column(Boolean, default=True, nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    ultima_consulta_em = Column(DateTime(timezone=True), nullable=True)

    movimentacoes = relationship(
        "Movimentacao", back_populates="processo", cascade="all, delete-orphan"
    )
    consultas_log = relationship(
        "ConsultaLog", back_populates="processo", cascade="all, delete-orphan"
    )

import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Movimentacao(Base):
    __tablename__ = "movimentacoes"
    __table_args__ = (
        UniqueConstraint("processo_id", "hash_dedup", name="uq_processo_hash_dedup"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    processo_id = Column(
        UUID(as_uuid=True), ForeignKey("processos.id", ondelete="CASCADE"), nullable=False
    )
    data_hora = Column(DateTime(timezone=True), nullable=False)

    codigo_movimento = Column(Integer, nullable=True)
    nome_movimento = Column(String, nullable=False)

    hash_dedup = Column(String(64), nullable=False)

    raw_payload = Column(JSONB, nullable=True)
    capturado_em = Column(DateTime(timezone=True), server_default=func.now())

    processo = relationship("Processo", back_populates="movimentacoes")
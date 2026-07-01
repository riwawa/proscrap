import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class ConsultaLog(Base):
    """Log de execuções de consulta à API DataJud, para observabilidade (ver S6)."""

    __tablename__ = "consultas_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    processo_id = Column(
        UUID(as_uuid=True), ForeignKey("processos.id", ondelete="CASCADE"), nullable=True
    )
    executado_em = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), nullable=True)  # success | error | no_change
    movimentacoes_novas = Column(Integer, default=0)
    erro_detalhe = Column(Text, nullable=True)

    processo = relationship("Processo", back_populates="consultas_log")

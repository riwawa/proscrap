import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class MovimentacaoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    data_hora: datetime
    codigo_movimento: int | None
    nome_movimento: str
    raw_payload: dict[str, Any] | None
    capturado_em: datetime
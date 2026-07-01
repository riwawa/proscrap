import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class ProcessoCreate(BaseModel):
    numero_cnj: str
    apelido: str | None = None

    @field_validator("numero_cnj")
    @classmethod
    def validar_formato_cnj(cls, v: str) -> str:
        # Validação leve de formato; regra completa fica no service layer (S1/S2).
        digits = "".join(c for c in v if c.isdigit())
        if len(digits) != 20:
            raise ValueError(
                "numero_cnj deve conter 20 dígitos no padrão CNJ "
                "(NNNNNNN-DD.AAAA.J.TR.OOOO)"
            )
        return v


class ProcessoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    numero_cnj: str
    tribunal_alias: str
    apelido: str | None
    ativo: bool
    criado_em: datetime
    ultima_consulta_em: datetime | None

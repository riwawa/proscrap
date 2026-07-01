"""
Lógica de deduplicação de movimentações processuais.


"""
import hashlib
from datetime import datetime


def calcular_hash_dedup(
    data_hora: datetime,
    codigo_movimento: int | None,
    nome_movimento: str,
) -> str:
    chave = f"{data_hora.isoformat()}|{codigo_movimento}|{nome_movimento}"
    return hashlib.sha256(chave.encode("utf-8")).hexdigest()


def parse_data_ajuizamento(raw: str) -> datetime:
    """
    Converte o campo `dataAjuizamento` do payload DataJud para datetime.
    vem no formato YYYYMMDDHHmmss (sem separadores),
    """
    return datetime.strptime(raw, "%Y%m%d%H%M%S")
"""
Service de sincronização de movimentações processuais.

Fluxo (ver ADR-003 no masterplan):
  1. Recebe um processo cadastrado
  2. Consulta a API DataJud via DataJudClient
  3. Normaliza os movimentos retornados
  4. Calcula hash de dedup para cada um (ADR-004 revisado pós S0)
  5. Insere apenas os registros novos (UNIQUE constraint garante idempotência)
  6. Registra o resultado em consultas_log
  7. Atualiza ultima_consulta_em no processo
"""
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.consulta_log import ConsultaLog
from app.models.movimentacao import Movimentacao
from app.models.processo import Processo
from app.services.datajud_client import DataJudClient, DataJudAuthError, DataJudTribunalNaoSuportadoError
from app.services.dedup import calcular_hash_dedup


def _normalizar_data_hora(raw: str) -> datetime:
    """
    Converte dataHora dos movimentos (ISO 8601 com Z) para datetime aware UTC.
    Confirmado no S0: formato '2025-02-12T17:50:36.000Z'.
    """
    return datetime.fromisoformat(raw.replace("Z", "+00:00"))


def sincronizar_processo(processo: Processo, db: Session) -> dict:
    """
    Consulta o DataJud para o processo informado e persiste as movimentações novas.
    Retorna um dict com status e quantidade de movimentações novas inseridas.
    """
    client = DataJudClient()
    status = "success"
    movimentacoes_novas = 0
    erro_detalhe = None

    try:
        # número sem formatação (20 dígitos) para a query Elasticsearch
        numero_sem_fmt = "".join(c for c in processo.numero_cnj if c.isdigit())
        payload = client.consultar_processo(processo.tribunal_alias, numero_sem_fmt)

        hits = payload.get("hits", {}).get("hits", [])
        if not hits:
            status = "no_change"
        else:
            fonte = hits[0].get("_source", {})
            movimentos = fonte.get("movimentos", [])

            for i, mov in enumerate(movimentos):
                raw_data_hora = mov.get("dataHora")
                if not raw_data_hora:
                    continue

                data_hora = _normalizar_data_hora(raw_data_hora)
                codigo = mov.get("codigo")  # int, confirmado no S0
                nome = mov.get("nome", "")

                hash_dedup = calcular_hash_dedup(data_hora, codigo, nome)

                movimentacao = Movimentacao(
                    processo_id=processo.id,
                    data_hora=data_hora,
                    codigo_movimento=codigo,
                    nome_movimento=nome,
                    hash_dedup=hash_dedup,
                    raw_payload=mov,
                )

                try:
                    db.add(movimentacao)
                    db.flush()  # detecta violação de UNIQUE antes do commit
                    movimentacoes_novas += 1
                except IntegrityError:
                    db.rollback()  # já existe — ignora e continua
                    # reinicia a sessão para o próximo insert
                    db.begin()

            if movimentacoes_novas == 0:
                status = "no_change"

        # atualiza ultima_consulta_em
        processo.ultima_consulta_em = datetime.now(timezone.utc)
        db.add(processo)

    except DataJudAuthError as e:
        status = "error"
        erro_detalhe = str(e)
        db.rollback()
    except DataJudTribunalNaoSuportadoError as e:
        status = "error"
        erro_detalhe = str(e)
        db.rollback()
    except Exception as e:
        status = "error"
        erro_detalhe = str(e)
        db.rollback()

    # log da execução
    log = ConsultaLog(
        processo_id=processo.id,
        status=status,
        movimentacoes_novas=movimentacoes_novas,
        erro_detalhe=erro_detalhe,
    )
    db.add(log)
    db.commit()

    return {
        "status": status,
        "movimentacoes_novas": movimentacoes_novas,
        "erro_detalhe": erro_detalhe,
    }
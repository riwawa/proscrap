"""
Cliente para a API Pública DataJud (CNJ).

Autenticação confirmada (ADR-005): API Key pública global, header
"Authorization: APIKey <chave>". A chave pode mudar a qualquer momento sem
aviso formal do CNJ — por isso o tratamento explícito de 401 abaixo.

Fonte: https://datajud-wiki.cnj.jus.br/api-publica/acesso/
"""
import httpx

from app.core.config import get_settings
from app.core.tribunal_endpoints import TRIBUNAL_ENDPOINTS

settings = get_settings()


class DataJudAuthError(Exception):
    """Levantado quando a API Key do DataJud é rejeitada (provável rotação pelo CNJ)."""


class DataJudTribunalNaoSuportadoError(Exception):
    """Levantado quando o alias do tribunal não está no mapeamento conhecido."""


class DataJudClient:
    def __init__(self, api_key: str | None = None, timeout: float = 90.0):
        self.api_key = api_key or settings.datajud_api_key
        self.timeout = timeout

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"APIKey {self.api_key}",
            "Content-Type": "application/json",
        }

    def consultar_processo(self, tribunal_alias: str, numero_processo_sem_formatacao: str) -> dict:
        """
        Consulta um processo pelo número CNJ (sem formatação, 20 dígitos) em um
        tribunal específico. Retorna o JSON bruto da resposta do Elasticsearch.

        NOTA (S0): o parsing/normalização dos `movimentos` ainda não foi validado
        com dados reais — fica para a sessão de spike.
        """
        url = TRIBUNAL_ENDPOINTS.get(tribunal_alias)
        if url is None:
            raise DataJudTribunalNaoSuportadoError(
                f"Tribunal '{tribunal_alias}' não está no mapeamento de endpoints conhecidos."
            )

        body = {"query": {"match": {"numeroProcesso": numero_processo_sem_formatacao}}}

        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(url, headers=self._headers(), json=body)

        if response.status_code == 401:
            raise DataJudAuthError(
                "API Key do DataJud rejeitada (401). A chave pode ter sido rotacionada "
                "pelo CNJ — verifique https://datajud-wiki.cnj.jus.br/api-publica/acesso/"
            )

        response.raise_for_status()
        return response.json()

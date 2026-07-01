"""
Configuração central da aplicação.
Lê variáveis de ambiente via pydantic-settings.
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # App
    app_name: str = "DataJud Monitor"
    environment: str = "development"
    debug: bool = True

    # Database
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/datajud_monitor"

    # Redis / Celery
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"

    # API Pública DataJud (CNJ)
    # ATENÇÃO: a chave é pública e global (não por tribunal/usuário), mas pode ser
    # alterada pelo CNJ a qualquer momento sem aviso prévio. Ver ADR-005 no masterplan.
    # Chave vigente sempre em: https://datajud-wiki.cnj.jus.br/api-publica/acesso/
    datajud_api_key: str = ""
    datajud_base_url: str = "https://api-publica.datajud.cnj.jus.br"

    # Agendamento (Celery Beat)
    consulta_diaria_hora_utc: int = 6  # horário (UTC) de disparo da task diária

    # Rate limiting (ver Riscos no masterplan: ~30 req/min observado, não documentado)
    datajud_rate_limit_per_minute: int = 25  # margem de segurança abaixo do observado


@lru_cache
def get_settings() -> Settings:
    return Settings()

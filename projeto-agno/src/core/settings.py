"""
Configurações centralizadas do projeto.
Carrega variáveis de ambiente e expõe um objeto de settings global.
"""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações do projeto Agno."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ─── Projeto ──────────────────────────────────────────────
    app_name: str = "Projeto Agno"
    app_version: str = "0.1.0"
    debug: bool = False

    # ─── Modelos de IA ────────────────────────────────────────
    google_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None

    # Modelo padrão
    default_model_provider: str = "google"   # "google" | "openai" | "anthropic"
    default_gemini_model: str = "gemini-2.5-flash"
    default_openai_model: str = "gpt-4o-mini"

    # ─── Ferramentas ──────────────────────────────────────────
    tavily_api_key: Optional[str] = None

    # ─── Banco de dados ───────────────────────────────────────
    db_url: Optional[str] = None
    sqlite_db_file: str = "data/agno.db"

    # ─── Servidor ─────────────────────────────────────────────
    host: str = "0.0.0.0"
    port: int = 7777


@lru_cache
def get_settings() -> Settings:
    """Retorna instância cacheada das configurações."""
    return Settings()


# Atalho global
settings = get_settings()

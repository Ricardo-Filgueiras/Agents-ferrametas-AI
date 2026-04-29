"""
Factory de modelos de IA.

Centraliza a criação dos modelos para evitar repetição em cada agent.
Basta importar get_model() e passar o provedor desejado.
"""

from typing import Literal

from src.core.settings import settings

ModelProvider = Literal["google", "openai", "anthropic"]


def get_model(
    provider: ModelProvider | None = None,
    model_id: str | None = None,
):
    """
    Retorna uma instância do modelo de IA configurado.

    Args:
        provider: Provedor do modelo. Se None, usa o padrão do settings.
        model_id: ID específico do modelo. Se None, usa o padrão do settings.

    Returns:
        Instância do modelo compatível com Agno.

    Raises:
        ValueError: Se o provedor não for suportado.
    """
    provider = provider or settings.default_model_provider

    if provider == "google":
        from agno.models.google import Gemini
        return Gemini(id=model_id or settings.default_gemini_model)

    if provider == "openai":
        from agno.models.openai import OpenAIChat
        return OpenAIChat(id=model_id or settings.default_openai_model)

    if provider == "anthropic":
        from agno.models.anthropic import Claude
        return Claude(id=model_id or "claude-3-5-sonnet-20241022")

    raise ValueError(f"Provedor '{provider}' não suportado. Use: google, openai, anthropic")

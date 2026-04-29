"""
LLMFactory — cria instâncias de LLM por provider com cache.

Usar lru_cache evita recriar clientes em cada chamada (custo de conexão),
mas ainda permite trocar provider/model sem reiniciar o app.
"""
from functools import lru_cache

from langchain_core.language_models import BaseChatModel


@lru_cache(maxsize=8)
def _criar_ollama(model: str, streaming: bool) -> BaseChatModel:
    from langchain_ollama import ChatOllama
    return ChatOllama(model=model, temperature=0, streaming=streaming)


@lru_cache(maxsize=8)
def _criar_openai(model: str, streaming: bool) -> BaseChatModel:
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model=model, temperature=0, streaming=streaming)


class LLMFactory:
    """
    Cria LangChain ChatModels por provider.

    Uso:
        llm = LLMFactory.create(provider="ollama", model="llama3.2:3b")
        llm = LLMFactory.create(provider="openai", model="gpt-4o-mini")
    """

    PROVIDER_MAP = {
        "ollama": _criar_ollama,
        "openai": _criar_openai,
    }

    # Mapeamento de nomes de UI para chaves internas
    UI_TO_KEY = {
        "Ollama (Local)": "ollama",
        "OpenAI": "openai",
    }

    @classmethod
    def create(
        cls,
        provider: str,
        model: str,
        streaming: bool = False,
    ) -> BaseChatModel:
        """
        Args:
            provider: "ollama" | "openai"  (ou nome da UI como "Ollama (Local)")
            model: nome do modelo, ex: "llama3.2:3b" ou "gpt-4o-mini"
            streaming: se True, ativa streaming de tokens
        """
        key = cls.UI_TO_KEY.get(provider, provider)
        factory_fn = cls.PROVIDER_MAP.get(key)
        if factory_fn is None:
            raise ValueError(
                f"Provider desconhecido: '{provider}'. "
                f"Disponíveis: {list(cls.PROVIDER_MAP.keys())}"
            )
        return factory_fn(model=model, streaming=streaming)

from src.core.interfaces import ILlmProvider
from src.core.config import config
from src.providers.gemini import GeminiProvider
from src.providers.openai_compatible import OpenAICompatibleProvider
import logging

logger = logging.getLogger(__name__)

class ProviderFactory:
    @staticmethod
    def get_provider(provider_name: str = None) -> ILlmProvider:
        name = provider_name or config.DEFAULT_PROVIDER
        
        if name.lower() == "gemini":
            return GeminiProvider()
        elif name.lower() == "deepseek":
            return OpenAICompatibleProvider(
                api_key=config.DEEPSEEK_API_KEY,
                base_url="https://api.deepseek.com/v1",
                model_name="deepseek-chat"
            )
        else:
            # Assume local ollama
            logger.info(f"Using local Ollama provider for model: {name}")
            return OpenAICompatibleProvider(
                api_key="ollama", # dummy key
                base_url=f"{config.OLLAMA_API_URL}/v1",
                model_name=name
            )

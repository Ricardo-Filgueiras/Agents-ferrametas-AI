import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from src.llm.config import OLLAMA_BASE_URL, DEFAULT_TEMPERATURE
from src.llm.model_manager import OllamaModelManager

load_dotenv()

class LLMFactory:
    @staticmethod
    def get_model(provider: str, model_name: str, temperature: float = None):
        """
        Retorna uma instância de chat model baseada no provider.
        
        Args:
            provider: "openai", "ollama", etc.
            model_name: Nome do modelo
            temperature: Temperatura da resposta (padrão: DEFAULT_TEMPERATURE)
        """
        if temperature is None:
            temperature = DEFAULT_TEMPERATURE
            
        if provider == "openai":
            return ChatOpenAI(
                model=model_name,
                temperature=temperature,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif provider == "ollama":
            return ChatOllama(
                model=model_name,
                temperature=temperature,
                base_url=OLLAMA_BASE_URL
            )
        else:
            raise ValueError(f"Provider {provider} não suportado.")
    
    @staticmethod
    def get_available_ollama_models():
        """Retorna lista de modelos Ollama disponíveis."""
        return OllamaModelManager.get_model_names()
    
    @staticmethod
    def is_ollama_available():
        """Verifica se Ollama está disponível."""
        return OllamaModelManager.is_ollama_available()

    @staticmethod
    def get_heavy_writer():
        # Modelo local para o trabalho pesado
        return LLMFactory.get_model("ollama", "llama3")

    @staticmethod
    def get_critical_reviewer():
        # Modelo potente para revisão e estratégia
        return LLMFactory.get_model("openai", "gpt-4o")

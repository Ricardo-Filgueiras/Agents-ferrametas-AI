import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

load_dotenv()

class LLMFactory:
    @staticmethod
    def get_model(provider: str, model_name: str, temperature: float = 0.7):
        """
        Retorna uma instância de chat model baseada no provider.
        """
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
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            )
        else:
            raise ValueError(f"Provider {provider} não suportado.")

    @staticmethod
    def get_heavy_writer():
        # Modelo local para o trabalho pesado
        return LLMFactory.get_model("ollama", "llama3")

    @staticmethod
    def get_critical_reviewer():
        # Modelo potente para revisão e estratégia
        return LLMFactory.get_model("openai", "gpt-4o")

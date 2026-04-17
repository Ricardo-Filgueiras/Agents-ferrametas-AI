import os
import logging
from typing import Optional, Any, Generator
from langchain_ollama import ChatOllama
from app.core.base import BaseLLM

class OllamaLLM(BaseLLM):
    """Implementador do LLM via Ollama usando LangChain."""
    
    def __init__(self, model_name: Optional[str] = None):
        self.logger = logging.getLogger("OllamaLLM")
        model = model_name or os.getenv("LLM_MODEL", "llama3.2:3b")
        base_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        
        self.logger.info(f"Conectando ao Ollama: {model} em {base_url}")
        self.llm = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=0.3
        )

    def ask(self, text: str, history: Optional[Any] = None) -> str:
        # A lógica de histórico será gerenciada pelo Controller
        try:
            response = self.llm.invoke(text)
            return response.content
        except Exception as e:
            self.logger.error(f"Erro no Ollama: {e}")
            return "Desculpe, tive um problema ao processar sua pergunta."

    def stream(self, text: str, history: Optional[Any] = None) -> Generator[str, None, None]:
        try:
            for chunk in self.llm.stream(text):
                yield chunk.content
        except Exception as e:
            self.logger.error(f"Erro no stream do Ollama: {e}")
            yield "Erro no processamento."

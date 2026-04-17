import os
import logging
from typing import Optional, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.base import BaseLLM

class GeminiLLM(BaseLLM):
    """Implementador do LLM via Google Gemini usando LangChain."""

    def __init__(self, model_name: Optional[str] = None):
        self.logger = logging.getLogger("GeminiLLM")
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY não encontrada no ambiente.")
            
        model = model_name or os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        
        self.logger.info(f"Conectando ao Google Gemini: {model}")
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=0.3
        )

    def ask(self, text: str) -> str:
        try:
            response = self.llm.invoke(text)
            return response.content
        except Exception as e:
            self.logger.error(f"Erro ao processar com Gemini: {str(e)}")
            return f"Erro ao processar com Gemini: {str(e)}"

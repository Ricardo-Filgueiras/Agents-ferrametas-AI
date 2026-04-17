import os
import logging
from typing import Optional
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from app.core.base import BaseLLM

class AgentController(BaseLLM):
    """Cérebro da Nova: Gerencia Prompts, Memória e suporta múltiplos Providers (Ollama, Gemini, etc)."""
    
    def __init__(self):
        self.logger = logging.getLogger("AgentController")
        provider = os.getenv("LLM_PROVIDER", "ollama").lower()
        model = os.getenv("LLM_MODEL", "llama3.2:3b")
        temperature = float(os.getenv("TEMPERATURE", "0.6"))
        
        # 1. Seleção Dinâmica do Provider
        if provider == "google" or provider == "gemini":
            self.logger.info(f"Usando Provider: Google Gemini ({model})")
            self.llm = ChatGoogleGenerativeAI(
                model=model,
                temperature=temperature,
                google_api_key=os.getenv("GOOGLE_API_KEY")
            )
        else:
            self.logger.info(f"Usando Provider: Ollama Local ({model})")
            self.llm = ChatOllama(
                model=model,
                temperature=temperature,
                base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434")
            )
        
        # 2. Configuração de Prompt e Memória (Idêntica para ambos)
        system_prompt = self._load_personality()
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ])
        
        self.history = ChatMessageHistory()
        self.chain = prompt_template | self.llm
        
        self.orchestrator = RunnableWithMessageHistory(
            self.chain,
            lambda session_id: self.history,
            input_messages_key="input",
            history_messages_key="history",
        )

    def _load_personality(self) -> str:
        path = "app/models/prompts/system.md"
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return "Você é a Nova, uma assistente de voz local."

    def ask(self, text: str, session_id: str = "nova_session") -> str:
        try:
            response = self.orchestrator.invoke(
                {"input": text},
                config={"configurable": {"session_id": session_id}}
            )
            return response.content
        except Exception as e:
            self.logger.error(f"Erro no Controller: {e}")
            return "Sinto muito, tive um erro ao processar minha resposta."

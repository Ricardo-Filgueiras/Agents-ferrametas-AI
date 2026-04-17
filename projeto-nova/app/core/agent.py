import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from app.models.prompts import NOVA_PROMPT

load_dotenv()

class VoiceAgent:
    """Orquestrador LangChain para a Nova com suporte a memória e histórico."""
    
    def __init__(self, model_name: Optional[str] = None):
        # Carrega configuração do .env
        model = model_name or os.getenv("LLM_MODEL", "llama3.2:3b")
        
        # Configuração do modelo Ollama
        self.llm = ChatOllama(
            model=model,
            temperature=0.7,
            base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434")
        )
        
        # Armazenamento simples de histórico em memória (pode ser evoluído para SQLite/Redis)
        self.history = ChatMessageHistory()
        
        # Criação da Chain usando LCEL
        self.chain = NOVA_PROMPT | self.llm
        
        # Wrapper para gerenciar o histórico automaticamente
        self.agent_with_chat_history = RunnableWithMessageHistory(
            self.chain,
            lambda session_id: self.history,
            input_messages_key="input",
            history_messages_key="history",
        )

    def ask(self, text: str, session_id: str = "default"):
        """Envia uma pergunta para a Nova e retorna a resposta contextualizada."""
        try:
            response = self.agent_with_chat_history.invoke(
                {"input": text},
                config={"configurable": {"session_id": session_id}}
            )
            return response.content
        except Exception as e:
            return f"Erro ao processar com Ollama: {str(e)}"

    def clear_history(self):
        """Limpa a memória da conversa atual."""
        self.history.clear()

import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from langchain_core.messages import SystemMessage
from src.schemas.state import AgentState
from src.llm.config import list_ollama_models, validate_model, get_system_prompt_for_agent


from dotenv import load_dotenv
from langchain.chat_models import init_chat_model


# Carrega variáveis do arquivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "data/checkpoints.db")

list_models = list_ollama_models()
print("Modelos Ollama disponíveis:", list_models)
print("Modelo selecionado:",list_models[0] )


def get_model():
    """
    Inicializa o modelo de chat baseado na variável de ambiente MODEL_NAME.
    Padrão para Ollama local "ollama:granite4.1:3b" se não especificado.
    Voce tem acesso a ferramentas.
    """
    model_name = os.getenv("MODEL_NAME", "ollama:llama3.2:3b")
    return init_chat_model(model_name)

# Configurações globais

# Carrega a Personalidade do Agente (System Message) do arquivo Markdown
SYSTEM_PROMPT = get_system_prompt_for_agent("strategist")



# Inicializa o modelo vinculado às ferramentas
model = get_model()

def call_llm(state: AgentState) -> AgentState:
    """
    Nó que chama a LLM injetando a System Message e o histórico atual.
    O modelo agora é capaz de chamar ferramentas.
    """
    # Adicionamos a SystemMessage no topo da lista de mensagens para a LLM
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(state["messages"])
    
    llm_result = model.invoke(messages)
    return {"messages": [llm_result]}

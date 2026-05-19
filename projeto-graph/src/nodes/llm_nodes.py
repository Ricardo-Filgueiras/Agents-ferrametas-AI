from langchain_core.messages import SystemMessage
from src.core.state import AgentState
from src.core.config import get_model, SYSTEM_PROMPT
from src.nodes.tools_node import tools

# Inicializa o modelo vinculado às ferramentas
model = get_model().bind_tools(tools)

def call_llm(state: AgentState) -> AgentState:
    """
    Nó que chama a LLM injetando a System Message e o histórico atual.
    O modelo agora é capaz de chamar ferramentas.
    """
    # Adicionamos a SystemMessage no topo da lista de mensagens para a LLM
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(state["messages"])
    
    llm_result = model.invoke(messages)
    return {"messages": [llm_result]}


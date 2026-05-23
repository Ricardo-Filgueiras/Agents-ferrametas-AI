from langchain_core.messages import SystemMessage
from src.schemas.state import AgentState
from src.llm.config import get_model, get_system_prompt_for_agent
from src.tools.caderno import write_note, read_notes
from langchain_core.runnables.config import RunnableConfig

# 1. Configuração de Personalidade
SYSTEM_PROMPT = get_system_prompt_for_agent("inspector")

# 2. Inicialização do Modelo com a ferramenta Caderno
tools = [write_note, read_notes]
model = get_model().bind_tools(tools)

def call_inspector(state: AgentState, config: RunnableConfig) -> AgentState:
    """
    Nó do Inspetor: Avalia o bolo e registra observações no caderno.
    """
    current_messages = list(state.get("messages", []))
    
    if not current_messages or not isinstance(current_messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + current_messages
    else:
        messages = current_messages

    response = model.invoke(messages, config=config)
    
    res_content = response.content
    updates = {"messages": [response]}
    
    if "ESTADO_NOTA:" in res_content:
        try:
            import re
            match = re.search(r"ESTADO_NOTA:\s*(\d+\.?\d*)", res_content)
            if match:
                updates["nota_inspetor"] = float(match.group(1))
        except:
            pass
            
    return updates

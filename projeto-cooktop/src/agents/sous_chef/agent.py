import os
from langchain_core.messages import SystemMessage
from src.schemas.state import AgentState
from src.llm.config import get_model, get_system_prompt_for_agent
from src.tools.kitchen_tools import search_recipes, control_oven, check_inventory
from langchain_core.runnables.config import RunnableConfig

# 1. Configuração de Personalidade
# O Sous Chef é o mestre da organização inicial da tigela
SYSTEM_PROMPT = get_system_prompt_for_agent("sous_chef")

# 2. Inicialização do Modelo com Ferramentas
tools = [search_recipes, control_oven, check_inventory]
model = get_model().bind_tools(tools)

def call_sous_chef(state: AgentState, config: RunnableConfig) -> AgentState:
    """
    Nó do Sous Chef: Ele analisa o pedido, busca receitas e organiza a tigela.
    """
    current_messages = list(state.get("messages", []))

    # Injeta a personalidade se for o início da conversa
    if not current_messages or not isinstance(current_messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + current_messages
    else:
        messages = current_messages

    # O modelo decide se precisa usar ferramentas ou apenas responder
    response = model.invoke(messages, config=config)
    
    # Lógica de extração de estado para a "Tigela"
    res_content = response.content
    updates = {"messages": [response]}
    
    if "ESTADO_TIGELA:" in res_content:
        try:
            import json
            import re
            # Busca o conteúdo entre colchetes []
            match = re.search(r'ESTADO_TIGELA:\s*(\[.*?\])', res_content)
            if match:
                ingredients = json.loads(match.group(1))
                updates["tigela"] = ingredients
        except:
            pass

    return updates


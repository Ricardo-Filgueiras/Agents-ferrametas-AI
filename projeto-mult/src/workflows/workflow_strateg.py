from langgraph.graph import END, START, StateGraph
from src.schemas.state import AgentState
from src.agents.strategist import call_llm as strategist_call_llm


def router_node(state: AgentState):
    """
    Decide se o grafo deve continuar para o nó de ferramentas ou terminar.
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    # Se a última mensagem da LLM tiver chamadas de ferramentas, vá para o nó "tools_node"
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools_node"
    
    # Caso contrário, termine a execução
    return END

def create_chat_graph():
    """
    Constrói e compila o grafo de chat com suporte a ferramentas.
    """
    # Define o StateGraph
    builder = StateGraph(AgentState)

    # Adiciona os nodes
    builder.add_node("agent", strategist_call_llm)

    # Define o fluxo
    builder.add_edge(START, "agent")
    
    # Adiciona aresta condicional da LLM para Ferramentas ou FIM
    
    # Após executar ferramentas, volta para a LLM para gerar a resposta final

    return builder.compile()

# Singleton do grafo para uso na aplicação
graph = create_chat_graph()
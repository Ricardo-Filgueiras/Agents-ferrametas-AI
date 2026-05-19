from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from src.core.state import AgentState
from src.nodes.llm_nodes import call_llm
from src.nodes.tools_node import tools_node
from src.core.config import DATABASE_URL
import os

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
    Constrói e compila o grafo de chat com persistência SQLite e suporte a ferramentas.
    """
    # Garante que o diretório do banco de dados existe
    os.makedirs(os.path.dirname(DATABASE_URL), exist_ok=True)
    
    # Define o StateGraph
    builder = StateGraph(AgentState)

    # Adiciona os nodes
    builder.add_node("call_llm", call_llm)
    builder.add_node("tools_node", tools_node)

    # Define o fluxo
    builder.add_edge(START, "call_llm")
    
    # Adiciona aresta condicional da LLM para Ferramentas ou FIM
    builder.add_conditional_edges(
        "call_llm",
        router_node,
        {
            "tools_node": "tools_node",
            END: END
        }
    )
    
    # Após executar ferramentas, volta para a LLM para gerar a resposta final
    builder.add_edge("tools_node", "call_llm")

    # Configura a persistência
    conn = sqlite3.connect(DATABASE_URL, check_same_thread=False)
    checkpointer = SqliteSaver(conn)
    
    return builder.compile(checkpointer=checkpointer)

# Singleton do grafo para uso na aplicação
graph = create_chat_graph()


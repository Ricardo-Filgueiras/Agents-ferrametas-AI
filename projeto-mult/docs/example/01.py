from typing import Dict, Any, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langgraph.prebuilt.tool_node import ToolNode

# 1. Definir o Estado do Grafo
class ArtigoState(TypedDict):
    tema: str
    pesquisa: str
    rascunho: str
    revisao: str
    aprovado: bool

# 2. Configurar o Modelo de Linguagem
llm = ChatOpenAI(model="gpt-4o")

# 3. Criar os Nós (Agentes)
def agente_pesquisador(state: ArtigoState):
    tema = state["tema"]
    # Aqui você pode usar Ferramentas de Busca (Tavily, Google, etc)
    pesquisa_feita = f"Dados e fatos recentes sobre: {tema}..."
    return {"pesquisa": pesquisa_feita}

def agente_redator(state: ArtigoState):
    tema = state["tema"]
    pesquisa = state["pesquisa"]
    prompt = f"Escreva um artigo técnico sobre {tema} usando a pesquisa: {pesquisa}"
    rascunho = llm.invoke(prompt).content
    return {"rascunho": rascunho}

def agente_revisor(state: ArtigoState):
    rascunho = state["rascunho"]
    prompt = f"Revise o seguinte artigo e diga se está pronto ou precisa de ajustes: {rascunho}"
    revisao = llm.invoke(prompt).content
    
    # Lógica simples de aprovação
    if "aprovado" in revisao.lower():
        return {"revisao": revisao, "aprovado": True}
    else:
        return {"revisao": revisao, "aprovado": False}

# 4. Condição de Decisão
def decidir_revisao(state: ArtigoState):
    if state["aprovado"]:
        return "aprovado"
    else:
        return "refazer"

# 5. Construir o Grafo
workflow = StateGraph(ArtigoState)

workflow.add_node("pesquisador", agente_pesquisador)
workflow.add_node("redator", agente_redator)
workflow.add_node("revisor", agente_revisor)

# Definir fluxo
workflow.set_entry_point("pesquisador")
workflow.add_edge("pesquisador", "redator")
workflow.add_edge("redator", "revisor")

workflow.add_conditional_edges(
    "revisor",
    decidir_revisao,
    {
        "aprovado": END,
        "refazer": "redator"
    }
)

app = workflow.compile()

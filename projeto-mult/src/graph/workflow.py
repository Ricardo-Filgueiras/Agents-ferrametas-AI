from langgraph.graph import StateGraph, END
from src.schemas.state import AgentState
from src.graph.nodes import (
    planning_node, 
    writing_node, 
    editing_node, 
    design_node, 
    validation_node
)

# Constante de controle (Lei nº 3 - Reduzida para desenvolvimento local)
MAX_REVISIONS = 1

def should_continue_editing(state: AgentState):
    """
    Roteador lógico: decide se volta para escrita ou segue para design.
    """
    review = state["review"]
    
    # Validação de segurança (Lei nº 2 - Reforçada para modelos locais)
    is_approved = False
    if review and hasattr(review, "is_approved"):
        is_approved = review.is_approved
    elif isinstance(review, str):
        # Se o modelo devolveu texto, tentamos inferir se foi aprovado
        is_approved = "aprovado" in review.lower() or "approved" in review.lower()

    if is_approved:
        print("--- REVIEW APPROVED: Moving to Design ---")
        return "design"
    
    if state["iteration_count"] >= MAX_REVISIONS:
        print("--- MAX REVISIONS REACHED: Moving to Design anyway ---")
        return "design"
    
    print(f"--- REVIEW REJECTED: Iteration {state['iteration_count']}/{MAX_REVISIONS} ---")
    return "writing"

def create_workflow():
    workflow = StateGraph(AgentState)

    # 1. Adicionar Nós
    workflow.add_node("planning", planning_node)
    workflow.add_node("writing", writing_node)
    workflow.add_node("editing", editing_node)
    workflow.add_node("design", design_node)
    workflow.add_node("validation", validation_node)

    # 2. Definir Conexões (Edges)
    workflow.set_entry_point("planning")
    
    workflow.add_edge("planning", "writing")
    workflow.add_edge("writing", "editing")

    # 3. Adicionar Lógica Condicional (Loop Editor -> Writer)
    workflow.add_conditional_edges(
        "editing",
        should_continue_editing,
        {
            "writing": "writing",
            "design": "design"
        }
    )

    workflow.add_edge("design", "validation")
    workflow.add_edge("validation", END)

    return workflow.compile()

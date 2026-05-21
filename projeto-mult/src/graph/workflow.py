from langgraph.graph import StateGraph, END
from src.schemas.state import AgentState
from src.graph.registry import WorkflowRegistry
from src.graph.nodes import (
    planning_node, 
    writing_node, 
    editing_node, 
    design_node, 
    validation_node,
    refinement_node
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
        is_approved = "aprovado" in review.lower() or "approved" in review.lower()

    if is_approved:
        print("--- REVIEW APPROVED: Moving to Design ---")
        return "design"
    
    if state["iteration_count"] >= MAX_REVISIONS:
        print("--- MAX REVISIONS REACHED: Moving to Design anyway ---")
        return "design"
    
    print(f"--- REVIEW REJECTED: Iteration {state['iteration_count']}/{MAX_REVISIONS} ---")
    return "writing"

def get_registry() -> WorkflowRegistry:
    """Configura e retorna o corpo do polvo com os tentáculos registrados."""
    registry = WorkflowRegistry()
    
    # Registrando os módulos na ordem desejada
    registry.register(name="planning", node_func=planning_node)
    registry.register(name="writing", node_func=writing_node, run_after="planning")
    registry.register(name="editing", node_func=editing_node, run_after="writing")
    registry.register(name="design", node_func=design_node, run_after="editing")
    registry.register(name="validation", node_func=validation_node, run_after="design")
    registry.register(name="refinement", node_func=refinement_node)
    
    return registry

def create_workflow():
    workflow = StateGraph(AgentState)
    registry = get_registry()
    modules = registry.get_modules_in_order()

    # 1. Adicionar todos os nós dinamicamente
    for mod in modules:
        workflow.add_node(mod.name, mod.node_func)

    # 2. Definir Conexões (Edges) de forma semi-dinâmica
    if modules:
        workflow.set_entry_point(modules[0].name)
        
        for i in range(len(modules) - 1):
            current_node = modules[i].name
            next_node = modules[i+1].name
            
            # Se for o nó de edição, aplicamos a regra condicional específica
            if current_node == "editing":
                workflow.add_conditional_edges(
                    current_node,
                    should_continue_editing,
                    {
                        "writing": "writing",
                        "design": next_node
                    }
                )
            else:
                # Conexão linear padrão
                workflow.add_edge(current_node, next_node)
                
        # O último nó vai para o FIM
        workflow.add_edge(modules[-1].name, END)

    return workflow.compile()


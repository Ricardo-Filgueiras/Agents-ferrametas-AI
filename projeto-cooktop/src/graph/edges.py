from src.schemas.state import AgentState
from langgraph.graph import END

def should_bake(state: AgentState) -> str:
    """
    Verifica se a massa está pronta para ir ao forno.
    """
    if state.get("status_massa") == "batida":
        return "bake_cake"
    return "mix_batter"

def evaluate_quality(state: AgentState) -> str:
    """
    Decide se o processo encerra ou se precisa de ajustes.
    """
    nota = state.get("nota_inspetor", 0)
    if nota < 7:
        return "gather_ingredients" # Volta para o início se estiver ruim
    return END

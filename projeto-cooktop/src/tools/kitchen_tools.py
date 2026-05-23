from langchain_core.tools import tool
from typing import List

@tool
def search_recipes(flavor: str) -> str:
    """Busca proporções e ingredientes corretos para um sabor específico de bolo."""
    # Placeholder para uma busca real ou lógica de negócio
    recipes = {
        "chocolate": "1 xícara de cacau, 2 xícaras de farinha, 3 ovos, 1 xícara de açúcar.",
        "baunilha": "2 xícaras de farinha, 3 ovos, 1 xícara de açúcar, 1 colher de sopa de essência de baunilha.",
        "cenoura": "3 cenouras, 2 xícaras de farinha, 3 ovos, 1 xícara de óleo."
    }
    return recipes.get(flavor.lower(), f"Receita básica para {flavor}: 2 xícaras de farinha, 2 ovos, 1 xícara de leite.")

@tool
def control_oven(temperature: int) -> str:
    """Liga ou ajusta a temperatura do forno."""
    if temperature > 250:
        return "Erro: Temperatura muito alta! O forno suporta até 250°C."
    return f"Forno ajustado para {temperature}°C. Pré-aquecimento iniciado."

@tool
def check_inventory(ingredients: List[str]) -> str:
    """Verifica se os ingredientes solicitados estão disponíveis no estoque."""
    # Simulação de estoque robusta (normalizada para minúsculas e singular)
    available = ["farinha", "ovo", "açúcar", "leite", "cacau", "óleo", "cenoura", "manteiga", "essência de baunilha"]
    
    missing = []
    for ing in ingredients:
        # Normalização básica: remove 's' no final para lidar com plural (ex: ovos -> ovo)
        # E remove espaços extras
        ing_normalized = ing.lower().strip()
        if ing_normalized.endswith('s') and ing_normalized[:-1] in available:
            continue
        if ing_normalized in available:
            continue
        missing.append(ing)
    
    if not missing:
        return "Todos os ingredientes estão disponíveis."
    return f"Faltam os seguintes ingredientes: {', '.join(missing)}."

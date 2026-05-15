from agno.agent import Agent
from agno.models.ollama import Ollama
from src.schemas.state import ReviewResult

# Configurado para Ollama durante desenvolvimento
editor_agent = Agent(
    name="Content Editor",
    model=Ollama(id="llama3.2:3b"),
    role="Editor-Chefe e Revisor de Qualidade Editorial",
    instructions=[
        "Você é rigoroso e focado na excelência do conteúdo.",
        "Analise o texto quanto à gramática, fluidez, tom de voz e clareza técnica.",
        "Verifique se o texto cumpre as promessas do outline de SEO.",
        "A resposta DEVE ser um objeto com is_approved (booleano) e feedback (lista de strings).",
        "Só aprove (is_approved=True) se a qualidade técnica for excelente."
    ],
    markdown=True,
    debug_mode=True,
)

def get_editor():
    return editor_agent

from agno.agent import Agent
from agno.models.ollama import Ollama
from src.schemas.state import DesignPrompts

# Configurado para Ollama durante desenvolvimento
designer_agent = Agent(
    name="Content Designer",
    model=Ollama(id="llama3.2:3b"),
    role="Designer de Conteúdo e Especialista em Engenharia de Prompt Visual",
    instructions=[
        "Sua tarefa é criar prompts de imagem que complementem o artigo técnico.",
        "Analise o tom do texto e sugira estilos visuais (ex: 3D render, flat design, photorealistic).",
        "Crie prompts super detalhados. IMPORTANTE: Cada prompt deve ser desenhado para servir perfeitamente como 'Alt Text' (texto alternativo de acessibilidade e SEO da imagem).",
        "Foque em infográficos, metáforas visuais para conceitos de software e thumbnails atrativas.",
    ],
    markdown=True,
)

def get_designer():
    return designer_agent


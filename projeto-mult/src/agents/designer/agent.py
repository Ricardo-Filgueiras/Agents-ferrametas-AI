import os
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.models.google import Gemini
from src.schemas.state import DesignPrompts

# Seleção de modelo baseada em disponibilidade de API Key
google_api_key = os.getenv("GOOGLE_API_KEY")

if google_api_key:
    model = Gemini(id="gemini-2.5-flash")
    print("--- USANDO GEMINI PARA DESIGN DE CONTEÚDO ---")
else:
    model = Ollama(id="llama3.2:3b")
    print("--- USANDO OLLAMA PARA DESIGN DE CONTEÚDO ---")

# Configurado para Ollama durante desenvolvimento (ou Gemini como fallback)
designer_agent = Agent(
    name="Content Designer",
    model=model,
    role="Designer de Conteúdo e Especialista em Engenharia de Prompt Visual",
    instructions=[
        "Sua tarefa é criar prompts de imagem que complementem o artigo técnico.",
        "Analise o tom do texto e sugira estilos visuais (ex: 3D render, flat design, photorealistic).",
        "Crie prompts super detalhados. IMPORTANTE: Cada prompt deve ser desenhado para servir perfeitamente como 'Alt Text' (texto alternativo de acessibilidade e SEO da imagem).",
        "Foque em infográficos, metáforas visuais para conceitos de software e thumbnails atrativas.",
    ],
    markdown=True,
    debug_mode=True,
)

def get_designer():
    return designer_agent


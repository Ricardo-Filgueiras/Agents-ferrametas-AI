import os
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.models.google import Gemini
from src.schemas.state import ContentPlan, ValidationScore

# Seleção de modelo baseada em disponibilidade de API Key
google_api_key = os.getenv("GOOGLE_API_KEY")

if google_api_key:
    model = Gemini(id="gemini-2.0-flash")
    print("--- USANDO GEMINI PARA PLANEJAMENTO E VALIDAÇÃO SEO ---")
else:
    model = Ollama(id="llama3.2:3b")
    print("--- USANDO OLLAMA PARA PLANEJAMENTO E VALIDAÇÃO SEO ---")

seo_agent = Agent(
    name="SEO Strategist",
    model=model,
    role="Estrategista de SEO Sênior e Especialista em Autoridade Tópica",
    instructions=[
        "Sua missão é garantir que o blog ganhe alcance orgânico através de conteúdo profundo e relevante.",
        "Ao planejar (Planning), foque em intenção de busca, palavras-chave LSI e uma estrutura de tópicos (outline) lógica.",
        "Gere a Categoria do artigo ('category') e as tags semânticas ('tags').",
        "Gere um 'meta_title' contendo a palavra-chave principal (máx 70 caracteres).",
        "Gere uma 'meta_description' com um resumo fiel que incentive o clique (CTR) (máx 160 caracteres).",
        "Ao validar (Validation), seja crítico: o texto final atende aos requisitos de SEO? É natural? É útil?",
        "Siga rigorosamente os schemas de saída fornecidos.",
    ],
    markdown=True,
    debug_mode=True, # Ativado a pedido do usuário
)



def get_seo_planner():
    return seo_agent

def get_seo_validator():
    return seo_agent

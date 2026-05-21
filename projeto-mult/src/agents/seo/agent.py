import os
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.models.google import Gemini
from src.schemas.state import ContentPlan, ValidationScore

# Seleção de modelo baseada em disponibilidade de API Key
google_api_key = os.getenv("GOOGLE_API_KEY")

if google_api_key:
    model = Gemini(id="gemini-2.5-flash")
    print("--- USANDO GEMINI (POTENTE) PARA PLANEJAMENTO E REFINAMENTO DE IDEIAS ---")
else:
    model = Ollama(id="llama3.2:3b")
    print("--- AVISO: GEMINI INDISPONÍVEL. USANDO OLLAMA PARA PLANEJAMENTO ---")

seo_agent = Agent(
    name="SEO Strategist",
    model=model,
    role="Estrategista de SEO Sênior e Arquiteto de Conteúdo",
    instructions=[
        "Sua missão principal é receber uma ideia bruta e transformá-la em um plano de conteúdo de elite.",
        "1. MELHORE A IDEIA: Se o usuário der um tema vago, torne-o específico, atraente e tecnicamente viável.",
        "2. REFINAMENTO DE KEYWORDS: Escolha as melhores palavras-chave (Primárias e LSI) que garantam autoridade tópica.",
        "3. ESTRUTURAÇÃO: Crie um outline (H1, H2, H3) que seja didático e otimizado.",
        "4. CTR: Gere um 'meta_title' e 'meta_description' que chamem a atenção.",
        "Siga rigorosamente o schema 'ContentPlan' para a saída.",
    ],
    markdown=True,
    debug_mode=True,
)




def get_seo_planner(model=None):
    if model:
        # Cria uma nova instância com o modelo desejado
        return Agent(
            name="SEO Strategist",
            model=model,
            role=seo_agent.role,
            instructions=seo_agent.instructions,
            markdown=True
        )
    return seo_agent

def get_seo_validator(model=None):
    if model:
        return Agent(
            name="SEO Validator",
            model=model,
            role=seo_agent.role,
            instructions=seo_agent.instructions,
            markdown=True
        )
    return seo_agent

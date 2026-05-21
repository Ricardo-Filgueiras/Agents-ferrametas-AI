import os
from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.models.google import Gemini
from src.schemas.state import Draft

# Seleção de modelo baseada em disponibilidade de API Key
google_api_key = os.getenv("GOOGLE_API_KEY")

# O Writer PRIORIZA o modelo local para economizar tokens na geração de volume
# Tenta usar Ollama, se não estiver disponível, usa Gemini como fallback
try:
    model = Ollama(id="llama3.2:3b")
    print("--- USANDO OLLAMA (LOCAL) PARA ESCRITA TÉCNICA (ECONOMIA DE TOKENS) ---")
except Exception:
    if google_api_key:
        model = Gemini(id="gemini-2.5-flash")
        print("--- FALLBACK: USANDO GEMINI PARA ESCRITA TÉCNICA ---")
    else:
        model = Ollama(id="llama3.2:3b") # Fallback final


# O Writer usa o modelo local para a escrita pesada (ou Gemini como fallback potente)
writer_agent = Agent(
    name="Technical Writer",
    model=model,
    role="Redator Técnico Especialista em Escrita Didática e Storytelling",
    instructions=[
        "Você transforma outlines de SEO em artigos técnicos profundos e envolventes.",
        "Sua escrita deve ser clara, direta e livre de 'enchimento'.",
        "REGRA DE OURO 1: NUNCA use termos vagos ou batidos como 'Guia Definitivo' ou 'Tudo o que você precisa saber'.",
        "REGRA DE OURO 2: O conteúdo DEVE incluir obrigatoriamente Tabelas ou Blocos de Código para facilitar a leitura e engajamento.",
        "Crie um 'excerpt' (resumo curto de 2-3 frases) em texto simples (sem markdown) para o card do blog.",
        "Use Markdown para formatar o texto (H2, H3, bold, listas).",
        "Garanta que todos os pontos técnicos do outline sejam cobertos.",
        "Mantenha um tom profissional, mas acessível.",
    ],
    markdown=True,
    debug_mode=True,
)

def get_technical_writer(model=None):
    if model:
        return Agent(
            name="Technical Writer",
            model=model,
            role=writer_agent.role,
            instructions=writer_agent.instructions,
            markdown=True
        )
    return writer_agent


"""
Agente Pesquisador

Especializado em busca e síntese de informações da web.
Utiliza Tavily para pesquisa aprofundada com suporte a múltiplas fontes.
"""

from agno.agent import Agent
from agno.tools.tavily import TavilyTools

from src.core.model_factory import get_model

pesquisador_agent = Agent(
    name="Agente Pesquisador",
    agent_id="pesquisador",
    model=get_model(),
    tools=[
        TavilyTools(
            search=True,
            max_results=5,
        ),
    ],
    markdown=True,
    instructions=[
        "Você é um pesquisador especialista em síntese de informações.",
        "Sempre cite suas fontes ao final da resposta.",
        "Organize as informações em tópicos claros e objetivos.",
        "Priorize fontes recentes e confiáveis.",
        "Se não encontrar informações suficientes, informe claramente ao usuário.",
    ],
    show_tool_calls=True,
    add_datetime_to_messages=True,
)

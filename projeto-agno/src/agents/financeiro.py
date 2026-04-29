"""
Agente Financeiro

Especializado em cotações de ações, dados de mercado e análise financeira.
Utiliza YFinance para dados históricos e Tavily para notícias em tempo real.
"""

from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.tools.yfinance import YFinanceTools

from src.core.model_factory import get_model

financeiro_agent = Agent(
    name="Agente Financeiro",
    agent_id="financeiro",
    model=get_model(),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            stock_fundamentals=True,
        ),
        TavilyTools(),
    ],
    markdown=True,
    instructions=[
        "Você é um assistente financeiro especializado em mercado de ações e dados financeiros.",
        "Sempre forneça dados atualizados com fontes confiáveis.",
        "Apresente os valores monetários sempre em BRL quando relevante.",
        "Ao analisar ações BR, use o sufixo correto (ex: PETR4.SA para Petrobras).",
        "Seja objetivo e forneça contexto de mercado quando possível.",
    ],
    show_tool_calls=True,
    add_datetime_to_messages=True,
)

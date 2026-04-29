from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.tavily import TavilyTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.tavily import TavilyTools
from dotenv import load_dotenv
load_dotenv()

agent = Agent(
    model=Gemini(id="gemini-2.5-flash"),
    tools=[TavilyTools(), YFinanceTools()],
    markdown=True,
    instructions="Você é um assistente financeiro especializado em fornecer informações sobre o mercado de ações e dados financeiros.",
    )


agent.print_response("Qual a cotação da empresa Petrobras atual ?", stream=True)
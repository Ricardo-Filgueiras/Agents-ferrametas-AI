from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.tavily import TavilyTools
from agno.tools.yfinance import YFinanceTools
from dotenv import load_dotenv
load_dotenv()

agent = Agent(
    model=Ollama(id="llama3.2:3b"),
    tools=[TavilyTools(), YFinanceTools()],
    markdown=True,
    instructions="Você é um assistente financeiro especializado em fornecer informações sobre o mercado de ações e dados financeiros.",
)

if __name__ == "__main__":
    agent.print_response("Qual a cotação da empresa Petrobras atual ?", stream=True)
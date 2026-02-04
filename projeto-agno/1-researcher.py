from agno.agent import Agent
from agno.models.google import Gemini
# from agno.tools.yfinance import YFinanceTools
from agno.tools.tavily import TavilyTools
from dotenv import load_dotenv
load_dotenv()

agent = Agent(
    model=Gemini(id="gemini-2.5-flash"),
    tools=[TavilyTools()],
    markdown=True
    )


agent.print_response("Qual a temperatura atual em Goiânia GO ?", stream=True)
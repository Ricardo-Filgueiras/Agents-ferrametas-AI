from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.openai import OpenAIResponses

agent = Agent(
    model=OpenAIResponses(id="gpt-4o", temperature=0.7),
    tools=[TavilyTools()], 
    markdown=True
    )


agent.print_response("Search tavily for 'language models'")
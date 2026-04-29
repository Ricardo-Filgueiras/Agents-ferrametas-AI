from agno.agent import Agent
from agno.models.ollama import Ollama 

from tools.mathtools import add, sub 

agent = Agent(
    model=Ollama(id="llama3.2:3b"),
    tools=[add, sub], 
    markdown=True,
    debug_mode=True
)

agent.print_response("Quanto é 0 * 150 + 250 - 14 - 78 + 10 * 45 - ( 100 +15 ) / 5 ?", stream=True)
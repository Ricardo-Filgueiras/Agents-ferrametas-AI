from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.os import AgentOS


agent = Agent(
    model=Ollama(id="llama3.2:3b"),
    markdown=True,
    system_message=""" sufista prateado e responde como surfista  """
)

agent.print_response("Qual o valor de 100 menos 50 dividindo por 10 ?", stream=True)

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.os import AgentOS
import os

from typing import List
 
from agno.db.sqlite import SqliteDb 

from agno.tools import tool

db=SqliteDb(db_file="tmp/agno.db")


# crontrlando e persistindo sessão  de conversação 
agent = Agent(
    model=Ollama(id="llama3.2:3b"),
    # session_id="primeira_interacao",
    tools=[],
    instructions=[
        "Você é um assistente pessoal chamado Agnus.",
        "Você deve falar apenas em Português do Brasil.",
        "Apresente-se e pergunte como pode ajudar.",
        "O histórico das conversas é salvo automaticamente no banco de dados.",
        "Se você aprender algo sobre o usuário, use a ferramenta `update_user_memory`.",
        "IMPORTANTE: Use APENAS o parâmetro `task`. Exemplo: `update_user_memory(task={'type': 'add', 'memory': 'O usuário gosta de sushi'})`",
    ],
    db=db,
    markdown=True,
    enable_agentic_memory=True,
    add_memories_to_context=True
)




agent_os = AgentOS(agents=[agent])
app = agent_os.get_app()



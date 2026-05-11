from agno.os import AgentOS
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.ollama import Ollama

agent = Agent(
    name="Agno Local Agent",
    model=Ollama(id="llama3.2:3b"),
    db=SqliteDb(db_file="agno.db"),
    add_history_to_context=True,
    markdown=True,
)

agent_os = AgentOS(agents=[agent])
app = agent_os.get_app()

if __name__ == "__main__":
    import uvicorn
    # Servindo o agente localmente para economizar tokens
    uvicorn.run(app, host="0.0.0.0", port=8000)
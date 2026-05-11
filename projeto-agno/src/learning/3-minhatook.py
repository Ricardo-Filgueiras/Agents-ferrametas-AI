from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.tavily import TavilyTools
from dotenv import load_dotenv
load_dotenv()

def minhaferramenta(veiculo: str) -> str:
    """
    Encontra o filtro automotivo para o veículo pesquisado.
    
    Esta função busca e recupera o filtro automotivo apropriado
    baseado nas especificações do veículo fornecidas.
    
    Args:
        veiculo (str): O modelo ou especificação do veículo
        
    Returns:
        str: Informações do filtro automotivo para o veículo pesquisado.
    """
    return f"Filtro automotivo encontrado para: {veiculo}"

agent = Agent(
    model=Ollama(id="llama3.2:3b"),
    tools=[TavilyTools(), minhaferramenta],
    markdown=True
)

if __name__ == "__main__":
    agent.print_response("Qual o filtro de Combustivel para Uno mile 4p 2010 ?", stream=True)
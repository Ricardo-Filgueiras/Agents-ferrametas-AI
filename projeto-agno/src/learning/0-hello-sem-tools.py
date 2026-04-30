from agno.agent import Agent
from agno.models.ollama import Ollama 


agent = Agent(
    model=Ollama(id="llama3.2:3b"),
    markdown=True
)

# agent.print_response("Quanto é 1 + 1 * 4 - (2 + 1) qual o valor desse calculo ?", stream=True)
# agent.print_response("Quanto é 0 * 150 + 250 - 14 - 78 + 10 * 45 - ( 100 +15 ) / 5 ?", stream=True)
# agent.print_response("Qual o valor de 100 menos 50 dividindo por 10 ?", stream=True)
# agent.print_response("Quanto é 5, mais 5 elevado a 2 mais 90 dividido por 3 ?", stream=True)
agent.print_response(
    """ Uma ONG está organizando kits de doação para distribuir em comunidades.

        No início do dia, já havia 5 kits prontos no estoque.

        Durante a manhã, 5 voluntários trabalharam na montagem, e cada um conseguiu montar 5 kits, totalizando uma produção de 5² kits.

        À tarde, a ONG recebeu uma doação de 90 itens individuais, que foram organizados em kits dividindo igualmente entre 3 equipes, resultando em novos kits prontos.

        Ao final do dia, quantos kits a ONG tem disponíveis para distribuição?
 """, 
    stream=True)
from src.tools.calcula_tools import TOOLS, TOOLS_BY_NAME
from pydantic import ValidationError
from langchain_core.messages import AIMessage, ToolMessage
from src.core.state import AgentState

# Catálogo com todas as ferramentas disponíveis para o agente
tools = TOOLS 

def tools_node(state: AgentState) -> AgentState:
    """
    Executa as chamadas de ferramentas e anexa os resultados (ou erros) como ToolMessages.
    Se ocorrer um erro, ele retorna uma instrução para a LLM corrigir a chamada.
    Suporta chamadas de ferramentas paralelas executando todas em sequência.
    """
    llm_response = state["messages"][-1]

    # Verifica se a última mensagem é da LLM e se tem chamadas de ferramentas
    if not isinstance(llm_response, AIMessage) or not getattr(llm_response, "tool_calls", None):
        return state

    tool_messages = []
    
    # Processa cada chamada de ferramenta (suporta chamadas em paralelo)
    for call in llm_response.tool_calls:
        name, args, id_ = call["name"], call["args"], call["id"]

        try:
            # Invoca a ferramenta correspondente com os argumentos fornecidos
            content = TOOLS_BY_NAME[name].invoke(args)
            status = "success"
        except (KeyError, IndexError, TypeError, ValueError, ValidationError) as e:
            # Captura erros de validação e execução para devolver à LLM para autocorreção
            content = f'Please, fix your error: {str(e)}.'
            status = "error"

        # Constrói a mensagem de resposta da ferramenta
        tool_messages.append(
            ToolMessage(
                name=name,
                content=str(content),
                tool_call_id=id_,
                status=status
            )
        )
    
    return {"messages": tool_messages}

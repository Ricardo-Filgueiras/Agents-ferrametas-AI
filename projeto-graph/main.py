import uuid
from langchain_core.messages import HumanMessage
from src.graphs.chat_graph import graph
from rich import print
from rich.markdown import Markdown

def run_cli():
    """
    Loop principal da CLI para interagir com o agente.
    """
    # Gera um thread_id único para esta sessão ou usa um fixo para testes
    # Para persistência entre reinicializações, use um ID constante ou pergunte ao usuário.
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    print(Markdown(f"# LangGraph Agent CLI\nSessão iniciada: `{thread_id}`"))
    print("Digite 'q' ou 'quit' para sair.\n")

    while True:
        try:
            user_input = input("Você: ")
            
            if user_input.lower() in ["q", "quit"]:
                print("\n[bold red]Bye 👋[/bold red]")
                break

            print(Markdown("---"))

            # Cria a mensagem do usuário
            human_message = HumanMessage(user_input)

            # Executa o grafo (chama a LLM e gerencia o estado)
            # O checkpointer SQLite salva o progresso automaticamente
            result = graph.invoke({"messages": [human_message]}, config=config)

            # Extrai e exibe a resposta
            last_message = result["messages"][-1]
            
            if hasattr(last_message, "usage_metadata") and last_message.usage_metadata:
                print(f"[dim]Tokens: {last_message.usage_metadata}[/dim]")
            
            print(Markdown(str(last_message.content)))
            print(Markdown("---"))
            
        except KeyboardInterrupt:
            print("\nEncerrando...")
            break
        except Exception as e:
            print(f"[bold red]Erro:[/bold red] {e}")

if __name__ == "__main__":
    run_cli()

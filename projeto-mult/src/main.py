import uuid
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from src.agent import graph
from rich import print
from rich.markdown import Markdown

def run_cli():
    """
    Loop principal da CLI para interagir com o agente.
    """
    # Gera um thread_id único para esta sessão ou usa um fixo para testes
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

            # Executa o grafo em modo streaming para capturar cada transição de estado e nó
            stream = graph.stream({"messages": [human_message]}, config=config)
            
            last_message = None
            for event in stream:
                for node_name, state_update in event.items():
                    # Exibe qual nó do grafo foi executado
                    if node_name == "call_llm":
                        import os
                        model_name = os.getenv("MODEL_NAME", "ollama:llama3.2:3b")
                        print(f"[bold blue]>>> Nó Executado: {node_name}[/bold blue] [dim]({model_name})[/dim]")
                    else:
                        print(f"[bold blue]>>> Nó Executado: {node_name}[/bold blue]")
                    
                    # Analisa as mensagens geradas por este nó
                    messages = state_update.get("messages", [])
                    for msg in messages:
                        if isinstance(msg, AIMessage):
                            # Se a LLM chamou alguma ferramenta
                            if msg.tool_calls:
                                for tc in msg.tool_calls:
                                    print(f"  [yellow]🛠️ Chamando ferramenta:[/yellow] [cyan]{tc['name']}[/cyan] com args: {tc['args']}")
                            if msg.content:
                                last_message = msg
                                
                        elif isinstance(msg, ToolMessage):
                            # Se o nó retornou o resultado de uma ferramenta
                            status = getattr(msg, "status", "success")
                            status_color = "green" if status == "success" else "red"
                            print(f"  [magenta]📥 Retorno da ferramenta ({msg.name}):[/magenta] [{status_color}]{msg.content}[/{status_color}]")

            # Exibe o resultado final após a execução de todos os nós
            if last_message:
                print(Markdown("---"))
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
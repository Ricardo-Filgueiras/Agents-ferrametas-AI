import sys
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from src.agent import graph
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

# Força o Rich a utilizar ASCII caso o terminal não suporte caracteres especiais complexos
console = Console(legacy_windows=True)

def print_message(sender: str, text: str, color: str):
    """Exibe mensagens formatadas no console usando Rich Panels."""
    panel = Panel(
        Text(text, style=color),
        title=f"[bold]{sender}[/bold]",
        title_align="left",
        border_style=color,
        expand=False
    )
    console.print(panel)

def main():
    console.clear()
    console.print(Panel.fit(
        "[bold cyan]LANGGRAPH - CHAT INTERATIVO LOCAL (OFFLINE)[/bold cyan]\n"
        "[dim]Converse com seu agente diretamente no terminal, livre de dependencias do LangSmith.[/dim]",
        border_style="cyan"
    ))
    
    # Estado inicial contendo o histórico de mensagens
    state = {"messages": []}
    
    console.print("[yellow]Digite 'sair' ou 'exit' para encerrar a conversa.[/yellow]\n")
    
    while True:
        try:
            user_input = Prompt.ask("[bold green]Voce[/bold green]")
            if user_input.strip().lower() in ["sair", "exit"]:
                console.print("\n[yellow]Encerrando a conversa. Ate mais! Bye.[/yellow]")
                break
                
            if not user_input.strip():
                continue
                
            # Adiciona a mensagem do usuário ao histórico do estado
            state["messages"].append(HumanMessage(content=user_input))
            
            console.print("\n[dim]Processando fluxo de nos do agente...[/dim]")
            
            # Invoca o grafo completo e obtém o estado atualizado
            result = graph.invoke(state)
            
            # Atualiza o estado da conversa com o novo histórico completo
            state = result
            
            # Exibe os retornos das mensagens recém-geradas (a última ou últimas na lista)
            last_messages = state["messages"]
            
            # Filtra apenas as mensagens geradas na última iteração para exibir no chat
            new_msgs = []
            for msg in reversed(last_messages):
                if isinstance(msg, HumanMessage) and msg.content == user_input:
                    break
                new_msgs.insert(0, msg)
            
            for msg in new_msgs:
                if isinstance(msg, AIMessage):
                    # Se tiver chamadas de ferramentas
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        for tool_call in msg.tool_calls:
                            print_message(
                                "FERRAMENTA (Chamando)",
                                f"Nome: {tool_call['name']}\nArgumentos: {tool_call['args']}",
                                "magenta"
                            )
                    if msg.content:
                        print_message("AGENTE", msg.content, "cyan")
                elif isinstance(msg, ToolMessage):
                    print_message(
                        f"RESPOSTA DA FERRAMENTA ({msg.name})",
                        msg.content,
                        "purple"
                    )
            console.print()
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Encerrando a conversa. Ate mais! Bye.[/yellow]")
            break
        except Exception as e:
            console.print(f"[bold red]Ocorreu um erro durante a execucao: {e}[/bold red]\n")

if __name__ == "__main__":
    main()

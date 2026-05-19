import os
import sys
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from src.agent import graph
from rich import print
from rich.panel import Panel
from rich.console import Console

console = Console()

def run_test():
    # Uma pergunta que requer múltiplos passos de cálculo para induzir o loop do agente ReAct:
    # 1. Soma: 10 + 5 = 15
    # 2. Multiplicação: 15 * 3 = 45
    # 3. Subtração: 45 - 5 = 40
    # 4. Divisão: 40 / 2 = 20
    prompt = "Some 10 e 5. Depois, multiplique o resultado por 3. Em seguida, subtraia 5. Por fim, divida o resultado por 2."
    
    console.print(Panel.fit(
        f"[bold green]Iniciando Teste do ReAct Agent com LangGraph[/bold green]\n\n"
        f"[bold]Pergunta:[/bold] {prompt}\n"
        f"[bold]Objetivo:[/bold] Observar o loop de execução (chama_llm -> tools -> chama_llm) no grafo.",
        title="LangGraph ReAct Loop Test"
    ))
    
    config = {"configurable": {"thread_id": "test-math-thread-123"}}
    
    # Executa o grafo em modo streaming para capturar cada transição de estado e chamadas de nó
    stream = graph.stream({"messages": [HumanMessage(content=prompt)]}, config=config)
    
    try:
        for event in stream:
            for node_name, state in event.items():
                if node_name == "call_llm":
                    import os
                    model_name = os.getenv("MODEL_NAME", "ollama:llama3.2:3b")
                    console.print(f"\n[bold blue]>>> Nó Executado: {node_name}[/bold blue] [dim]({model_name})[/dim]")
                else:
                    console.print(f"\n[bold blue]>>> Nó Executado: {node_name}[/bold blue]")
                
                messages = state.get("messages", [])
                for msg in messages:
                    if isinstance(msg, AIMessage):
                        if msg.tool_calls:
                            console.print("   [bold yellow]Llama chamou ferramenta(s):[/bold yellow]")
                            for tc in msg.tool_calls:
                                console.print(f"     - [cyan]{tc['name']}[/cyan] com argumentos: {tc['args']}")
                        if msg.content:
                            console.print(f"   [bold green]Llama respondeu:[/bold green] {msg.content}")
                            
                    elif isinstance(msg, ToolMessage):
                        console.print(f"   [bold magenta]Ferramenta ({msg.name}) retornou:[/bold magenta] {msg.content}")
                    
                    else:
                        console.print(f"   [dim]Mensagem do tipo {type(msg).__name__}:[/dim] {msg.content}")
                        
    except Exception as e:
        console.print(f"\n[bold red]Erro durante a execução:[/bold red] {e}")
        console.print("[yellow]Dica: Verifique se o seu modelo do Ollama (ou outro configurado no .env) está rodando e acessível.[/yellow]")

if __name__ == "__main__":
    run_test()

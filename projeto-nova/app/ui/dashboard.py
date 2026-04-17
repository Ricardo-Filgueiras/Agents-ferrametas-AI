from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from datetime import datetime
from app.core.state import AgentState

class Dashboard:
    """Interface de monitoramento profissional no terminal usando Rich."""
    
    def __init__(self, state: AgentState):
        self.state = state
        self.console = Console()

    def create_layout(self) -> Layout:
        """Define a estrutura visual do dashboard."""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", size=12),
            Layout(name="footer", size=6)
        )
        layout["main"].split_row(
            Layout(name="modules", ratio=1),
            Layout(name="metrics", ratio=1)
        )
        return layout

    def get_header(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="right", ratio=1)
        grid.add_row(
            Text("🎙️ NOVA AGENT - SISTEMA OPERACIONAL LOCAL", style="bold magenta"),
            Text(datetime.now().strftime("%H:%M:%S"), style="cyan")
        )
        return Panel(grid, style="white on blue")

    def get_modules_panel(self) -> Panel:
        table = Table(box=None, expand=True)
        table.add_column("Módulo", style="bold")
        table.add_column("Status", justify="right")
        
        for module, status in self.state.status.items():
            color = "green" if status == "OK" else "yellow" if status != "Idle" else "white"
            table.add_row(module.upper(), f"[{color}]{status}[/{color}]")
            
        return Panel(table, title="[bold]ESTADO DOS MÓDULOS[/bold]", border_style="cyan")

    def get_metrics_panel(self) -> Panel:
        table = Table(box=None, expand=True)
        table.add_column("Métrica", style="bold")
        table.add_column("Valor", justify="right")
        
        table.add_row("Latência Total", f"{self.state.total_latency:.2f}s")
        table.add_row("Ação Atual", f"[bold yellow]{self.state.current_action}[/bold yellow]")
        
        # Latências específicas
        for mod, lat in self.state.module_latencies.items():
            table.add_row(f"  > {mod}", f"{lat:.2f}s")
            
        return Panel(table, title="[bold]MÉTRICAS DE PERFORMANCE[/bold]", border_style="magenta")

    def get_footer(self) -> Panel:
        log_text = Text()
        log_text.append(f"ÚLTIMA ENTRADA: ", style="bold green")
        log_text.append(f"{self.state.last_input}\n", style="white")
        log_text.append(f"NOVA RESPONDEU: ", style="bold magenta")
        log_text.append(f"{self.state.last_output}", style="italic white")
        
        return Panel(log_text, title="[bold]ÚLTIMA INTERAÇÃO[/bold]", border_style="green")

    def run(self):
        """Inicia a renderização contínua em modo Live."""
        layout = self.create_layout()
        
        with Live(layout, refresh_per_second=4, console=self.console) as live:
            while self.state.is_running:
                layout["header"].update(self.get_header())
                layout["modules"].update(self.get_modules_panel())
                layout["metrics"].update(self.get_metrics_panel())
                layout["footer"].update(self.get_footer())

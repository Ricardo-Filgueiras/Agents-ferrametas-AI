from typing import Callable, Dict, List, Optional
from src.schemas.state import AgentState

class WorkflowModule:
    """Representa um 'Tentáculo' (Módulo) do nosso polvo."""
    def __init__(self, name: str, node_func: Callable[[AgentState], AgentState], run_after: Optional[str] = None):
        self.name = name
        self.node_func = node_func
        self.run_after = run_after

class WorkflowRegistry:
    """Gerenciador central de módulos (O corpo do polvo)."""
    def __init__(self):
        self.modules: Dict[str, WorkflowModule] = {}
        # Ordem lógica básica para garantir coerência
        self.execution_order: List[str] = []

    def register(self, name: str, node_func: Callable, run_after: Optional[str] = None):
        """Registra um novo módulo no sistema."""
        module = WorkflowModule(name, node_func, run_after)
        self.modules[name] = module
        
        # Lógica simples de ordenação baseada no 'run_after'
        if run_after and run_after in self.execution_order:
            idx = self.execution_order.index(run_after)
            self.execution_order.insert(idx + 1, name)
        else:
            self.execution_order.append(name)
            
    def get_modules_in_order(self) -> List[WorkflowModule]:
        """Retorna os módulos na ordem correta de execução."""
        return [self.modules[name] for name in self.execution_order]

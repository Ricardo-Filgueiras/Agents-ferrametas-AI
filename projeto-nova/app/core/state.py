from dataclasses import dataclass, field
from typing import Dict, Optional, List, Callable
import time

@dataclass
class AgentState:
    """Gerenciador de estado compartilhado para observabilidade (Thread-Safe)."""
    
    # Status por módulo (UI)
    status: Dict[str, str] = field(default_factory=lambda: {
        "audio": "Idle",
        "stt": "Idle",
        "llm": "Idle",
        "tts": "Idle"
    })
    
    # Métricas e Dados
    last_input: str = ""
    last_output: str = ""
    total_latency: float = 0.0
    module_latencies: Dict[str, float] = field(default_factory=dict)
    
    # Estado Geral
    is_running: bool = True
    current_action: str = "Aguardando Wake Word..."
    
    # Callbacks para eventos (opcional para desacoplamento futuro)
    _listeners: List[Callable] = field(default_factory=list, repr=False)

    def update_module(self, module: str, status: str, latency: Optional[float] = None):
        """Atualiza o status e a latência de um módulo específico."""
        if module in self.status:
            self.status[module] = status
        if latency is not None:
            self.module_latencies[module] = latency
        self._notify()

    def set_action(self, action: str):
        """Atualiza a ação atual sendo executada pelo sistema."""
        self.current_action = action
        self._notify()

    def log_interaction(self, user_input: str, agent_output: str, total_time: float):
        """Registra o resultado final de um ciclo de interação."""
        self.last_input = user_input
        self.last_output = agent_output
        self.total_latency = total_time
        self._notify()

    def subscribe(self, callback: Callable):
        """Assina um callback para ser notificado de mudanças de estado."""
        self._listeners.append(callback)

    def _notify(self):
        """Notifica os ouvintes sobre mudanças no estado."""
        for listener in self._listeners:
            try:
                listener(self)
            except Exception:
                pass

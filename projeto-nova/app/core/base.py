from abc import ABC, abstractmethod
import numpy as np

class BaseSTT(ABC):
    @abstractmethod
    def transcribe(self, audio_data: np.ndarray) -> str:
        """Converte áudio raw para texto."""
        pass

class BaseLLM(ABC):
    @abstractmethod
    def ask(self, text: str) -> str:
        """Processa texto e retorna resposta contextualizada."""
        pass

class BaseTTS(ABC):
    @abstractmethod
    def synthesize(self, text: str) -> str:
        """Converte texto para arquivo de áudio ou buffer."""
        pass

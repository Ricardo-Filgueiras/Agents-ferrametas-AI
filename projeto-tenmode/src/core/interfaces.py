from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from src.core.models import Message, ToolCall

class BaseTool(ABC):
    name: str
    description: str
    parameters_schema: dict

    @abstractmethod
    async def execute(self, **kwargs) -> str:
        """Executes the tool with given arguments and returns observation string."""
        pass

class ILlmProvider(ABC):
    @abstractmethod
    async def generate_response(
        self, 
        messages: List[Message], 
        system_prompt: Optional[str] = None,
        tools: Optional[List[BaseTool]] = None
    ) -> Tuple[Optional[str], Optional[ToolCall]]:
        """
        Returns either a final text response, or a ToolCall object.
        Tuple is (text_response, tool_call).
        """
        pass

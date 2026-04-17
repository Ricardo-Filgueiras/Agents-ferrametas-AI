from enum import Enum
from pydantic import BaseModel
from typing import Any, Dict

class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class Message(BaseModel):
    role: Role
    content: str
    
class Conversation(BaseModel):
    id: str
    user_id: str
    provider: str

class ToolCall(BaseModel):
    name: str
    arguments: Dict[str, Any]

class ToolResult(BaseModel):
    name: str
    content: str

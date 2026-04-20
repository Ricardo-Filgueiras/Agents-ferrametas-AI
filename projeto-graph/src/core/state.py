from collections.abc import Sequence
from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages

class AgentState(TypedDict):
    """
    O estado do agente, mantendo o histórico de mensagens.
    O reducer add_messages garante que novas mensagens sejam anexadas ao histórico.
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]

from openai import AsyncOpenAI
from typing import List, Optional, Tuple
from src.core.interfaces import ILlmProvider, BaseTool
from src.core.models import Message, ToolCall
from src.core.config import config
import json

class OpenAICompatibleProvider(ILlmProvider):
    def __init__(self, api_key: str, base_url: str, model_name: str):
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.model_name = model_name

    async def generate_response(
        self, 
        messages: List[Message], 
        system_prompt: Optional[str] = None,
        tools: Optional[List[BaseTool]] = None
    ) -> Tuple[Optional[str], Optional[ToolCall]]:
        
        oai_messages = []
        if system_prompt:
            oai_messages.append({"role": "system", "content": system_prompt})
            
        for msg in messages:
            oai_messages.append({"role": msg.role.value, "content": msg.content})

        openai_tools = None
        if tools:
            openai_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.parameters_schema
                    }
                } for t in tools
            ]

        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=oai_messages,
            tools=openai_tools,
            tool_choice="auto" if tools else None 
        )
        
        message = response.choices[0].message
        
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            args = json.loads(tool_call.function.arguments)
            return None, ToolCall(name=tool_call.function.name, arguments=args)
            
        return message.content, None

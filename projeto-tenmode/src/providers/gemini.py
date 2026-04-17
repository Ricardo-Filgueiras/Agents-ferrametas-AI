import google.generativeai as genai
from typing import List, Optional, Tuple
from src.core.interfaces import ILlmProvider, BaseTool
from src.core.models import Message, ToolCall
from src.core.config import config
import json

class GeminiProvider(ILlmProvider):
    def __init__(self):
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
    def _format_messages(self, messages: List[Message], system_prompt: Optional[str]) -> list:
        history = []
        if system_prompt:
            self.model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_prompt)
            
        for msg in messages:
            role = "user" if msg.role.value == "user" else "model"
            history.append({"role": role, "parts": [msg.content]})
        return history

    async def generate_response(
        self, 
        messages: List[Message], 
        system_prompt: Optional[str] = None,
        tools: Optional[List[BaseTool]] = None
    ) -> Tuple[Optional[str], Optional[ToolCall]]:
        
        system_instruction = system_prompt or ""
        if tools:
            tools_spec = [
                {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.parameters_schema
                } for t in tools
            ]
            system_instruction += "\n\nYou have access to these tools:\n" + json.dumps(tools_spec, indent=2)
            system_instruction += "\nIf you decide to use a tool, you MUST return ONLY a JSON block with this schema: {\"tool_name\": \"...\", \"arguments\": {...}}"

        history = self._format_messages(messages, system_instruction)
        
        response = await self.model.generate_content_async(history)
        text = response.text
        
        if "{" in text and "tool_name" in text:
            try:
                start = text.find("{")
                end = text.rfind("}") + 1
                json_str = text[start:end]
                data = json.loads(json_str)
                if "tool_name" in data and "arguments" in data:
                    return None, ToolCall(name=data["tool_name"], arguments=data["arguments"])
            except Exception:
                pass
                
        return text, None

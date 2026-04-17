import json
from typing import Optional
from src.core.models import Message, Role
from src.providers.factory import ProviderFactory

class SkillRouter:
    @staticmethod
    async def route(user_intent: str, available_skills: list[dict]) -> Optional[str]:
        if not available_skills:
            return None
            
        system_prompt = (
            "You are a Skill Router. Based on the user's input, choose the MOST appropriate skill from the available skills list. "
            "You MUST reply ONLY with a JSON object in this exact format: {\"skillName\": \"name_of_skill\"} or {\"skillName\": null} if none match.\n\n"
            "Available Skills:\n"
        )
        for s in available_skills:
            system_prompt += f"- {s['name']}: {s['description']}\n"
            
        provider = ProviderFactory.get_provider() # Default provider
        
        messages = [Message(role=Role.USER, content=user_intent)]
        text, _ = await provider.generate_response(messages=messages, system_prompt=system_prompt)
        
        if text:
            try:
                start = text.find("{")
                end = text.rfind("}") + 1
                json_str = text[start:end]
                data = json.loads(json_str)
                return data.get("skillName")
            except Exception:
                pass
        return None

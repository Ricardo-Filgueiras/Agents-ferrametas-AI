import logging
from typing import Optional
from src.core.models import Message, Role
from src.agent.loop import AgentLoop
from src.skills.executor import SkillExecutor
from src.memory.manager import MemoryManager

logger = logging.getLogger(__name__)

class AgentController:
    def __init__(self):
        self.memory = MemoryManager()

    async def handle_user_input(self, user_id: str, text: str) -> str:
        # Load or create conversation
        conv = await self.memory.get_or_create_conversation(str(user_id))
        
        # Load recent context
        messages = await self.memory.load_context(conv.id)
        
        user_msg = Message(role=Role.USER, content=text)
        messages.append(user_msg)
        
        # 1. Router Step
        skill_context = await SkillExecutor.get_skill_context(text)
        
        system_prompt = "You are ten, a local AI personal assistant."
        import os
        identity_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", ".agents", "identity.md"))
        if os.path.exists(identity_path):
            with open(identity_path, "r", encoding="utf-8") as f:
                system_prompt = f.read().strip()
                
        if skill_context:
            system_prompt += f"\n\n{skill_context}"
            
        # 2. Agent Loop
        loop = AgentLoop(provider_name=conv.provider)
        final_response = await loop.run(messages, system_prompt=system_prompt)
        
        assistant_msg = Message(role=Role.ASSISTANT, content=final_response)
        
        # 3. Save turn
        await self.memory.save_turn(conv.id, user_msg, assistant_msg)
        
        return final_response

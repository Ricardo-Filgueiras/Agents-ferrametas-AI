from typing import Optional
from src.skills.loader import SkillLoader
from src.skills.router import SkillRouter

class SkillExecutor:
    @staticmethod
    async def get_skill_context(user_intent: str) -> Optional[str]:
        skills = SkillLoader.load_skills()
        skill_name = await SkillRouter.route(user_intent, skills)
        
        if skill_name:
            for s in skills:
                if s["name"] == skill_name:
                    return f"Active Skill: {s['name']}\nInstructions:\n{s['content']}"
        return None

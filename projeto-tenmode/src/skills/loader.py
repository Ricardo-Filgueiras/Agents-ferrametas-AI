import os
import yaml
import logging

logger = logging.getLogger(__name__)

SKILLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", ".agents", "skills"))

class SkillLoader:
    @staticmethod
    def load_skills() -> list[dict]:
        skills = []
        if not os.path.exists(SKILLS_DIR):
            logger.warning(f"Skills directory not found: {SKILLS_DIR}")
            return skills
            
        for d in os.listdir(SKILLS_DIR):
            skill_path = os.path.join(SKILLS_DIR, d)
            if os.path.isdir(skill_path):
                md_path = os.path.join(skill_path, "SKILL.md")
                if os.path.exists(md_path):
                    with open(md_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            try:
                                metadata = yaml.safe_load(parts[1])
                                body = parts[2].strip()
                                skills.append({
                                    "folder": d,
                                    "name": metadata.get("name", d),
                                    "description": metadata.get("description", ""),
                                    "content": body
                                })
                            except yaml.YAMLError as e:
                                logger.error(f"Error parsing YAML for skill {d}: {e}")
        return skills

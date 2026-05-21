import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from langchain_core.messages import SystemMessage
from src.llm.config import list_ollama_models, validate_model, get_system_prompt_for_agent

a = list_ollama_models()
print(a)
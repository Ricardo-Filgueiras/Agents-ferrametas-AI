import os
from agno.models.ollama import Ollama
from agno.models.google import Gemini
from agno.models.openai import OpenAIChat

def resolve_model(model_tag: str):
    """
    Resolve um modelo baseado em uma tag (ex: 'gemini', 'ollama:llama3', 'openai:gpt-4o').
    """
    google_api_key = os.getenv("GOOGLE_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # 1. Casos explícitos com prefixo
    if model_tag.startswith("ollama:"):
        model_id = model_tag.split(":", 1)[1]
        return Ollama(id=model_id)
    
    if model_tag.startswith("openai:"):
        model_id = model_tag.split(":", 1)[1]
        return OpenAIChat(id=model_id)
    
    if model_tag.startswith("gemini:"):
        model_id = model_tag.split(":", 1)[1]
        return Gemini(id=model_id)

    # 2. Casos simplificados
    if model_tag == "gemini":
        if google_api_key:
            return Gemini(id="gemini-2.5-flash")
        return Ollama(id="llama3.2:3b") # Fallback local
    
    if model_tag == "ollama":
        return Ollama(id="llama3.2:3b")
    
    if model_tag == "openai":
        if openai_api_key:
            return OpenAIChat(id="gpt-4o-mini")
        return resolve_model("gemini") # Fallback cloud
    
    # 3. Default (se a tag for o próprio ID do Ollama ou algo desconhecido)
    return Ollama(id=model_tag)

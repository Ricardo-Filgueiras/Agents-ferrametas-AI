import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# Carrega variáveis do arquivo .env
load_dotenv()

def get_model():
    """
    Inicializa o modelo de chat baseado na variável de ambiente MODEL_NAME.
    Padrão para Ollama local llama3.2:3b se não especificado.
    """
    model_name = os.getenv("MODEL_NAME", "ollama:llama3.2:3b")
    return init_chat_model(model_name)

# Configurações globais
DATABASE_URL = os.getenv("DATABASE_URL", "data/checkpoints.db")

# Carrega a Personalidade do Agente (System Message) do arquivo Markdown
SYSTEM_PROMPT_PATH = os.path.join(os.path.dirname(__file__), "../..", ".agents", "system_prompt.md")

def load_system_prompt():
    try:
        with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Aviso: Não foi possível carregar o system_prompt.md: {e}")
        return "Você é um assistente de IA prestativo."

SYSTEM_PROMPT = load_system_prompt()

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_ALLOWED_USER_IDS = [
        int(x.strip()) for x in os.getenv("TELEGRAM_ALLOWED_USER_IDS", "").split(",") if x.strip()
    ]
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/v1")
    DEFAULT_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", os.getenv("DEFAULT_PROVIDER", "gemini"))
    MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "5"))
    MEMORY_WINDOW_SIZE = int(os.getenv("MEMORY_WINDOW_SIZE", "15"))
    DB_PATH = os.getenv("DB_PATH", "./data/db.sqlite")

config = Config()

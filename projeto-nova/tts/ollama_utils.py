import requests

def get_ollama_models():
    """Retorna uma lista de nomes de modelos disponíveis no Ollama local."""
    OLLAMA_BASE_URL = "http://localhost:11434"
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags")
        if response.status_code == 200:
            data = response.json()
            return [model['name'] for model in data.get('models', [])]
        else:
            print("❌ Erro ao conectar com Ollama")
            return []
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar ao Ollama. Certifique-se que o Ollama está rodando.")
        return []

if __name__ == "__main__":
    modelos = get_ollama_models()
    if modelos:
        print("✅ Modelos disponíveis:")
        for m in modelos:
            print(f"  - {m}")

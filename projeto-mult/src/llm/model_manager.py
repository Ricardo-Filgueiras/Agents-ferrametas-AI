import requests
from typing import List, Dict, Optional
from src.llm.config import OLLAMA_BASE_URL


class OllamaModelManager:
    """Gerenciador para listar e gerenciar modelos do Ollama."""
    
    @staticmethod
    def list_models() -> List[Dict[str, str]]:
        """
        Lista todos os modelos disponíveis no Ollama.
        
        Returns:
            Lista de dicionários com informações dos modelos.
            Exemplo: [{"name": "llama3.2", "size": "3.5 GB", ...}, ...]
        """
        try:
            response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
            response.raise_for_status()
            
            data = response.json()
            models = []
            
            if "models" in data:
                for model in data["models"]:
                    models.append({
                        "name": model.get("name", "unknown"),
                        "modified_at": model.get("modified_at", ""),
                        "size": OllamaModelManager._format_size(model.get("size", 0)),
                    })
            
            return sorted(models, key=lambda x: x["name"])
        
        except requests.exceptions.ConnectionError:
            return []
        except Exception as e:
            print(f"Erro ao listar modelos: {e}")
            return []
    
    @staticmethod
    def get_model_names() -> List[str]:
        """Retorna apenas os nomes dos modelos."""
        models = OllamaModelManager.list_models()
        return [model["name"] for model in models]
    
    @staticmethod
    def is_ollama_available() -> bool:
        """Verifica se o Ollama está disponível."""
        try:
            response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    @staticmethod
    def _format_size(bytes_size: int) -> str:
        """Formata tamanho em bytes para formato legível."""
        for unit in ["B", "KB", "MB", "GB"]:
            if bytes_size < 1024:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024
        return f"{bytes_size:.1f} TB"
    
    @staticmethod
    def pull_model(model_name: str) -> bool:
        """
        Faz download de um modelo do Ollama.
        
        Args:
            model_name: Nome do modelo (ex: "llama3.2:3b")
            
        Returns:
            True se bem-sucedido, False caso contrário.
        """
        try:
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/pull",
                json={"name": model_name},
                timeout=300  # 5 minutos
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Erro ao baixar modelo: {e}")
            return False

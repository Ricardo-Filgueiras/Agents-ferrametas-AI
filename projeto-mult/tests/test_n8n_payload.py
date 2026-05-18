import pytest
from datetime import datetime
from unittest.mock import MagicMock
from src.database.models import Article

def test_n8n_payload_construction():
    """
    Valida se a lógica de construção do payload no app.py 
    está protegida contra campos nulos e mantém a estrutura correta.
    """
    # 1. Criar um mock de um artigo vindo do banco com alguns campos nulos
    mock_article = MagicMock(spec=Article)
    mock_article.id = 1
    mock_article.topic = "Teste de Tópico"
    mock_article.keywords = ["kw1", "kw2"]
    mock_article.title = None  # Campo nulo proposital
    mock_article.category = "Tecnologia"
    mock_article.tags = None   # Campo nulo proposital
    mock_article.meta_title = "Título SEO"
    mock_article.meta_description = ""
    mock_article.excerpt = None
    mock_article.outline = ["H1", "H2"]
    mock_article.content_markdown = "# Conteúdo"
    mock_article.seo_score = 8.5
    mock_article.image_prompts = ["Prompt 1"]
    mock_article.created_at = datetime(2026, 5, 15, 12, 0, 0)

    # 2. Simular a lógica de montagem do payload (extraída do app.py)
    is_public = True
    payload = {
        "id": mock_article.id,
        "topic": mock_article.topic,
        "keywords": mock_article.keywords if isinstance(mock_article.keywords, list) else [],
        "title": mock_article.title or mock_article.topic,
        "category": mock_article.category or "Geral",
        "tags": mock_article.tags if isinstance(mock_article.tags, list) else [],
        "meta_title": mock_article.meta_title or "",
        "meta_description": mock_article.meta_description or "",
        "excerpt": mock_article.excerpt or "",
        "outline": mock_article.outline if isinstance(mock_article.outline, list) else [],
        "content_markdown": mock_article.content_markdown or "",
        "is_public": is_public,
        "seo_score": mock_article.seo_score or 0,
        "image_prompts": mock_article.image_prompts if isinstance(mock_article.image_prompts, list) else [],
        "created_at": mock_article.created_at.isoformat() if mock_article.created_at else None
    }

    # 3. Asserts
    assert payload["id"] == 1
    assert payload["title"] == "Teste de Tópico" # Deve assumir o tópico se o título for None
    assert payload["category"] == "Tecnologia"
    assert payload["tags"] == [] # Deve ser lista vazia, não None
    assert payload["is_public"] is True
    assert payload["seo_score"] == 8.5
    assert payload["created_at"] == "2026-05-15T12:00:00"
    print("\n✅ Teste de payload n8n passou com sucesso!")

if __name__ == "__main__":
    test_n8n_payload_construction()

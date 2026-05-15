import unittest
from src.database.repository import ArticleRepository
from src.schemas.state import AgentState, AgentExecutionLog

class TestArticleRepository(unittest.TestCase):
    def setUp(self):
        # Usa um banco de dados em memória para o teste não afetar a produção
        self.repo = ArticleRepository(db_url="sqlite:///:memory:")

    def test_save_agent_state_with_strings(self):
        """
        Testa se o repositório consegue salvar o estado mesmo quando 
        os agentes retornam strings puras em vez de objetos Pydantic 
        (simulando degradação de LLMs locais).
        """
        # Simulando um estado onde todos os objetos falharam e viraram strings
        mock_state: AgentState = {
            "topic": "Teste de Resiliência",
            "keywords": ["teste", "resiliência"],
            "plan": "Isso é uma string, não um ContentPlan object", # AQUI causava o erro do .title()
            "draft": "Rascunho de teste em formato string puro",
            "review": "Aprovado!",
            "design": "Prompt gerado como string",
            "validation": "85.5", # String que deveria ser objeto
            "is_validated": True,
            "iteration_count": 2,
            "logs": [],
            "current_step": "validation"
        }

        try:
            # Se isso funcionar, a nossa blindagem está perfeita!
            article_id = self.repo.save_agent_state(mock_state)
            self.assertIsNotNone(article_id)
            print(f"Sucesso! Artigo salvo no banco em memória com ID: {article_id}")
        except Exception as e:
            self.fail(f"O salvamento falhou. O repositório ainda está vulnerável. Erro: {e}")

if __name__ == '__main__':
    unittest.main()

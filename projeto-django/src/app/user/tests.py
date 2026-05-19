import tempfile
import os
from django.test import TransactionTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from app.user.models import Clientes, Documentos_clientes

class ObserverPatternSignalTest(TransactionTestCase):
    """
    Test suite for validating the Observer design pattern implemented via Django Signals.
    Ensures that uploading a file automatically triggers content extraction and generates AI analyses.
    """
    
    def setUp(self):
        # Create a test user first as Clientes has a foreign key to User
        self.user = User.objects.create_user(username="testuser", password="password123")
        # Create a test client
        self.cliente = Clientes.objects.create(
            tipo_cliente="PJ",
            nome="Empresa Teste SA",
            email="contato@empresateste.com",
            cpf_cnpj="12345678000190",
            user=self.user
        )
        
    def _wait_for_processing(self, documento, timeout=5):
        import time
        start_time = time.time()
        while time.time() - start_time < timeout:
            documento.refresh_from_db()
            if documento.arquivo_markdown and documento.analise_ia:
                return
            time.sleep(0.05)
        raise TimeoutError("O processamento assíncrono do documento demorou mais que o esperado.")
        
    def test_csv_upload_triggers_observer_processing(self):
        # 1. Prepare a simulated CSV file
        csv_content = b"Nome,Cargo,Salario\nAlice,Engenheira de IA,15000\nBob,Cientista de Dados,12000"
        csv_file = SimpleUploadedFile(
            name="colaboradores.csv",
            content=csv_content,
            content_type="text/csv"
        )
        
        # 2. Save the model instance. This triggers the post_save signal (Observer pattern)
        documento = Documentos_clientes.objects.create(
            cliente=self.cliente,
            nome="Colaboradores de Teste",
            arquivo=csv_file
        )
        
        # 3. Wait for asynchronous background processing
        self._wait_for_processing(documento)
        
        # 4. Assertions to confirm Observer Signal worked
        self.assertTrue(documento.arquivo_markdown)
        self.assertTrue(documento.analise_ia)
        self.assertIn("Processamento concluído com sucesso via Padrão de Projeto Observer", documento.analise_ia)
        self.assertIn("Tabelas de Dados Encontradas", documento.analise_ia)
        # Verify markdown table conversion
        self.assertIn("| Nome | Cargo | Salario |", documento.analise_ia)
        self.assertIn("| Alice | Engenheira de IA | 15000 |", documento.analise_ia)
        self.assertIn("| Bob | Cientista de Dados | 12000 |", documento.analise_ia)
        
        # Clean up files created during tests
        if documento.arquivo and os.path.exists(documento.arquivo.path):
            os.remove(documento.arquivo.path)
        if documento.arquivo_markdown and os.path.exists(documento.arquivo_markdown.path):
            os.remove(documento.arquivo_markdown.path)

    def test_markdown_upload_triggers_observer_processing(self):
        # 1. Prepare a simulated MD file
        md_content = b"# Documentacao IA\n\nEste e um arquivo markdown de teste."
        md_file = SimpleUploadedFile(
            name="docs_ia.md",
            content=md_content,
            content_type="text/markdown"
        )
        
        # 2. Trigger the Observer pattern
        documento = Documentos_clientes.objects.create(
            cliente=self.cliente,
            nome="Documentação IA",
            arquivo=md_file
        )
        
        # Wait for asynchronous background processing
        self._wait_for_processing(documento)
        
        # 3. Assertions
        self.assertTrue(documento.arquivo_markdown)
        self.assertTrue(documento.analise_ia)
        self.assertIn("Este e um arquivo markdown de teste.", documento.analise_ia)
        self.assertIn("Relatório de Processamento do Documento", documento.analise_ia)
        
        # Clean up files
        if documento.arquivo and os.path.exists(documento.arquivo.path):
            os.remove(documento.arquivo.path)
        if documento.arquivo_markdown and os.path.exists(documento.arquivo_markdown.path):
            os.remove(documento.arquivo_markdown.path)


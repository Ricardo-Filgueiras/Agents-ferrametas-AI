import json
from unittest.mock import patch
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from app.user.models import Clientes, Documentos_clientes
from app.nova.models import InteractionSession, InteractionMessage

class NovaAppTests(TestCase):
    def setUp(self):
        # Disconnect signal to avoid running background processing/docling during these test cases
        from django.db.models.signals import post_save
        from app.user.signals import post_save_documento_receptor
        post_save.disconnect(post_save_documento_receptor, sender=Documentos_clientes)

        # 1. Create a User and authenticate Client
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client = Client()
        self.client.login(username="testuser", password="testpassword")
        
        # 2. Create a Cliente scoped to this user
        self.cliente = Clientes.objects.create(
            user=self.user,
            nome="Ricardo Filgueiras",
            email="ricardo@example.com",
            cpf_cnpj="123.456.789-00",
            ativo=True
        )
        
        # 3. Create a Document associated with the client
        self.documento = Documentos_clientes.objects.create(
            cliente=self.cliente,
            nome="Planilha de Contas",
            arquivo="documentos/planilha.pdf",
            analise_ia=True
        )

    def tearDown(self):
        # Reconnect the signal to ensure subsequent test cases in the test suite run with signals active
        from django.db.models.signals import post_save
        from app.user.signals import post_save_documento_receptor
        post_save.connect(post_save_documento_receptor, sender=Documentos_clientes)

    def test_database_models_creation(self):
        """
        Tests creation and representation of InteractionSession and InteractionMessage.
        """
        session = InteractionSession.objects.create(
            cliente=self.cliente,
            documento=self.documento
        )
        self.assertEqual(str(session), f"Chat com Ricardo Filgueiras | Doc: Planilha de Contas")
        
        message = InteractionMessage.objects.create(
            session=session,
            sender="user",
            message="Qual o saldo total?"
        )
        self.assertEqual(str(message), "User: Qual o saldo total?...")

    def test_start_chat_from_doc_view(self):
        """
        Tests redirect to a created/retrieved session when initiating chat from document link.
        """
        url = reverse("nova:start_chat", kwargs={"doc_pk": self.documento.pk})
        response = self.client.get(url)
        
        # Asserts it redirects to the chat session console
        session = InteractionSession.objects.get(cliente=self.cliente, documento=self.documento)
        expected_redirect_url = reverse("nova:chat_session", kwargs={"session_id": session.id})
        self.assertRedirects(response, expected_redirect_url)

    def test_chat_session_view(self):
        """
        Tests loading the premium chat interface for an active session.
        """
        session = InteractionSession.objects.create(
            cliente=self.cliente,
            documento=self.documento
        )
        url = reverse("nova:chat_session", kwargs={"session_id": session.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "nova/chat.html")
        self.assertEqual(response.context["cliente"], self.cliente)
        self.assertEqual(response.context["documento"], self.documento)

    @patch("requests.post")
    def test_send_message_api_success(self, mock_post):
        """
        Tests posting messages and receiving a successful mocked Ollama response.
        """
        from unittest.mock import Mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "message": {
                "content": "O total pendente é R$ 264,00."
            }
        }
        mock_post.return_value = mock_response
        
        session = InteractionSession.objects.create(
            cliente=self.cliente,
            documento=self.documento
        )
        url = reverse("nova:send_message_api", kwargs={"session_id": session.id})
        
        post_data = {"message": "Quanto temos pendente?"}
        response = self.client.post(
            url,
            data=json.dumps(post_data),
            content_type="application/json"
        )
        
        self.assertEqual(response.status_code, 200)
        res_json = response.json()
        self.assertEqual(res_json["status"], "success")
        self.assertEqual(res_json["user_message"], "Quanto temos pendente?")
        self.assertEqual(res_json["assistant_response"], "O total pendente é R$ 264,00.")
        
        # Verify db persistence
        self.assertEqual(session.messages.filter(sender="user").count(), 1)
        self.assertEqual(session.messages.filter(sender="assistant").count(), 1)

    def test_send_message_api_empty_validation(self):
        """
        Tests API validation when posting an empty message.
        """
        session = InteractionSession.objects.create(
            cliente=self.cliente,
            documento=self.documento
        )
        url = reverse("nova:send_message_api", kwargs={"session_id": session.id})
        
        response = self.client.post(
            url,
            data=json.dumps({"message": "   "}),
            content_type="application/json"
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["status"], "error")

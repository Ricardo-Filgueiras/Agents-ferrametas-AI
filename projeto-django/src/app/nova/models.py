import uuid
from django.db import models
from app.user.models import Clientes, Documentos_clientes

class InteractionSession(models.Model):
    """
    Represents an interactive AI agent chat session.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, verbose_name="Cliente")
    documento = models.ForeignKey(Documentos_clientes, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Documento Focado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Sessão de Interação"
        verbose_name_plural = "Sessões de Interação"
        ordering = ["-updated_at"]

    def __str__(self):
        doc_info = f" | Doc: {self.documento.nome}" if self.documento else ""
        return f"Chat com {self.cliente.nome}{doc_info}"

class InteractionMessage(models.Model):
    """
    Stores individual messages of a chat session.
    """
    SENDER_CHOICES = (
        ("user", "Usuário"),
        ("assistant", "Nova (Assistente IA)"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(InteractionSession, on_delete=models.CASCADE, related_name="messages", verbose_name="Sessão")
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES, verbose_name="Remetente")
    message = models.TextField(verbose_name="Mensagem")
    context_used = models.TextField(blank=True, null=True, verbose_name="Contexto Utilizado (RAG)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Enviado em")

    class Meta:
        verbose_name = "Mensagem da Interação"
        verbose_name_plural = "Mensagens da Interação"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender.capitalize()}: {self.message[:40]}..."

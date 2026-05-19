import uuid
from django.db import models
from django.contrib.auth.models import User
from app.user.models import Clientes, Documentos_clientes

class ChatSession(models.Model):
    """
    Representa uma sessão de chat entre o usuário e o assistente (Nova).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, verbose_name="Cliente")
    documento = models.ForeignKey(Documentos_clientes, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Documento")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Sessão de Chat"
        verbose_name_plural = "Sessões de Chat"
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Chat {self.id} de {self.user.username}"

class ChatMessage(models.Model):
    """
    Armazena as mensagens individuais de uma sessão de chat.
    """
    SENDER_CHOICES = (
        ("user", "Usuário"),
        ("bot", "IA (Nova)"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages", verbose_name="Sessão")
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES, verbose_name="Remetente")
    message = models.TextField(verbose_name="Mensagem")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Enviado em")

    class Meta:
        verbose_name = "Mensagem do Chat"
        verbose_name_plural = "Mensagens do Chat"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender}: {self.message[:50]}"

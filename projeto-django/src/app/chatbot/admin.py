from django.contrib import admin
from .models import ChatSession, ChatMessage

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cliente', 'created_at', 'updated_at')
    list_filter = ('user', 'cliente', 'created_at')
    search_fields = ('id', 'user__username', 'cliente__nome')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('session', 'sender', 'message_preview', 'created_at')
    list_filter = ('sender', 'created_at')
    
    def message_preview(self, obj):
        return obj.message[:50]
    message_preview.short_description = 'Mensagem'

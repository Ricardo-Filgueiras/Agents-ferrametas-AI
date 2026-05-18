from django.contrib import admin
from .models import Clientes, Documentos_clientes

@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_cliente', 'email', 'cpf_cnpj', 'data_cadastro', 'ativo', 'user')
    list_filter = ('tipo_cliente', 'ativo', 'data_cadastro')
    search_fields = ('nome', 'email', 'cpf_cnpj')

@admin.register(Documentos_clientes)
class DocumentosClientesAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cliente', 'arquivo', 'arquivo_markdown', 'data_cadastro', 'ativo')
    list_filter = ('ativo', 'data_cadastro')
    search_fields = ('nome', 'cliente__nome')

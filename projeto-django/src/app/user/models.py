import uuid
import os
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from martor.models import MartorField


class Clientes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TIPO_CLIENTE = (
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    )

    tipo_cliente = models.CharField(max_length=2, choices=TIPO_CLIENTE, verbose_name='Tipo de Cliente')
    nome = models.CharField(max_length=100, verbose_name='Nome')
    email = models.EmailField(verbose_name='Email')
    cpf_cnpj = models.CharField(max_length=14, verbose_name='CPF/CNPJ')
    data_cadastro = models.DateField(auto_now_add=True, verbose_name='Data de Cadastro')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    
   
    def __str__(self):
        return self.nome   
         
class Documentos_clientes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, verbose_name='Cliente')
    nome = models.CharField(max_length=100, verbose_name='Nome')
    arquivo = models.FileField(
        upload_to='documentos/%Y/%m/%d', 
        verbose_name='Arquivo Original',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'xlsx', 'xls', 'csv', 'docx', 'md'])]
    )
    arquivo_markdown = models.FileField(upload_to='documentos/md/%Y/%m/%d', verbose_name='Arquivo Markdown (Docling)', blank=True, null=True)
    analise_ia = MartorField(verbose_name='Análise da IA', blank=True, null=True)
    data_cadastro = models.DateField(auto_now_add=True, verbose_name='Data de Cadastro')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    content = MartorField(verbose_name='Conteúdo Markdown Extraído', blank=True, null=True)
    
    @property
    def extensao(self):
        if not self.arquivo:
            return ""
        name, ext = os.path.splitext(self.arquivo.name)
        return ext.lower()

    def __str__(self):
        return self.nome
        
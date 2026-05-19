from django import forms
from .models import Clientes, Documentos_clientes

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['tipo_cliente', 'nome', 'email', 'cpf_cnpj', 'ativo']
        widgets = {
            'tipo_cliente': forms.Select(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Cliente'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
            'cpf_cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apenas números'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documentos_clientes
        fields = ['nome', 'arquivo', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Documento'}),
            'arquivo': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.pdf,.xlsx,.xls,.csv,.docx,.md'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_arquivo(self):
        arquivo = self.cleaned_data.get('arquivo')
        if arquivo:
            ext = arquivo.name.split('.')[-1].lower() if '.' in arquivo.name else ''
            if ext not in ['pdf', 'xlsx', 'xls', 'csv', 'docx', 'md']:
                raise forms.ValidationError("Extensão de arquivo não permitida. Por favor, envie arquivos PDF, Excel (.xlsx, .xls), CSV, Word (.docx) ou Markdown (.md).")
        return arquivo

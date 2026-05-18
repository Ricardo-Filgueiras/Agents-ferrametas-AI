from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Clientes, Documentos_clientes
from .forms import ClienteForm, DocumentoForm

# --- AUTH REGISTRATION ---
def register(request):
    if request.user.is_authenticated:
        return redirect('interface:home')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Conta criada com sucesso! Bem-vindo, {user.username}!")
            return redirect('interface:home')
        else:
            messages.error(request, "Erro no cadastro. Por favor, verifique os campos informados.")
    else:
        form = UserCreationForm()
        
    return render(request, 'registration/register.html', {'form': form})


# --- CLIENTES CRUD (USER SCOPED) ---
@login_required
def clientes_list(request):
    clientes = Clientes.objects.filter(user=request.user).order_by('-data_cadastro')
    return render(request, 'user/clientes_list.html', {'clientes': clientes})

@login_required
def clientes_detail(request, pk):
    cliente = get_object_or_404(Clientes, pk=pk, user=request.user)
    documentos = Documentos_clientes.objects.filter(cliente=cliente).order_by('-data_cadastro')
    return render(request, 'user/clientes_detail.html', {'cliente': cliente, 'documentos': documentos})

@login_required
def clientes_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.user = request.user
            cliente.save()
            messages.success(request, f"Cliente {cliente.nome} cadastrado com sucesso!")
            return redirect('user:clientes_list')
    else:
        form = ClienteForm()
    return render(request, 'user/clientes_form.html', {'form': form, 'title': 'Cadastrar Cliente'})

@login_required
def clientes_update(request, pk):
    cliente = get_object_or_404(Clientes, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, f"Cliente {cliente.nome} atualizado com sucesso!")
            return redirect('user:clientes_detail', pk=pk)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'user/clientes_form.html', {'form': form, 'title': 'Editar Cliente', 'cliente': cliente})

@login_required
def clientes_delete(request, pk):
    cliente = get_object_or_404(Clientes, pk=pk, user=request.user)
    if request.method == 'POST':
        nome = cliente.nome
        cliente.delete()
        messages.success(request, f"Cliente {nome} removido com sucesso!")
        return redirect('user:clientes_list')
    return render(request, 'user/clientes_confirm_delete.html', {'cliente': cliente})


# --- DOCUMENTOS CRUD (USER SCOPED) ---
@login_required
def documentos_list(request, cliente_pk):
    cliente = get_object_or_404(Clientes, pk=cliente_pk, user=request.user)
    documentos = Documentos_clientes.objects.filter(cliente=cliente).order_by('-data_cadastro')
    return render(request, 'user/documentos_list.html', {'cliente': cliente, 'documentos': documentos})

@login_required
def documentos_detail(request, cliente_pk, pk):
    cliente = get_object_or_404(Clientes, pk=cliente_pk, user=request.user)
    documento = get_object_or_404(Documentos_clientes, pk=pk, cliente=cliente)
    return render(request, 'user/documentos_detail.html', {'cliente': cliente, 'documento': documento})

@login_required
def documentos_create(request, cliente_pk):
    cliente = get_object_or_404(Clientes, pk=cliente_pk, user=request.user)
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.cliente = cliente
            documento.save()
            messages.success(request, f"Documento {documento.nome} carregado com sucesso!")
            return redirect('user:clientes_detail', pk=cliente_pk)
    else:
        form = DocumentoForm()
    return render(request, 'user/documentos_form.html', {'form': form, 'cliente': cliente, 'title': 'Adicionar Documento'})

@login_required
def documentos_update(request, cliente_pk, pk):
    cliente = get_object_or_404(Clientes, pk=cliente_pk, user=request.user)
    documento = get_object_or_404(Documentos_clientes, pk=pk, cliente=cliente)
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            form.save()
            messages.success(request, f"Documento {documento.nome} atualizado com sucesso!")
            return redirect('user:clientes_detail', pk=cliente_pk)
    else:
        form = DocumentoForm(instance=documento)
    return render(request, 'user/documentos_form.html', {'form': form, 'cliente': cliente, 'documento': documento, 'title': 'Editar Documento'})

@login_required
def documentos_delete(request, cliente_pk, pk):
    cliente = get_object_or_404(Clientes, pk=cliente_pk, user=request.user)
    documento = get_object_or_404(Documentos_clientes, pk=pk, cliente=cliente)
    if request.method == 'POST':
        nome = documento.nome
        documento.delete()
        messages.success(request, f"Documento {nome} removido com sucesso!")
        return redirect('user:clientes_detail', pk=cliente_pk)
    return render(request, 'user/documentos_confirm_delete.html', {'cliente': cliente, 'documento': documento})


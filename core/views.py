from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CustomUserCreationForm, iPhoneForm, iPhoneSearchForm
from .models import iPhone
from django.db.models import Q

@login_required
def cadastrar_iphone(request):
    if request.method == 'POST':
        form = iPhoneForm(request.POST)
        if form.is_valid():
            iphone = form.save(commit=False)
            if iphone.condicao == 'Novo':
                iphone.saude_bateria = None
            iphone.fornecedor = request.user  # Definindo o fornecedor como o usuário logado
            iphone.save()
            messages.success(request, 'iPhone cadastrado com sucesso.')
            return redirect('cadastrar_iphone')
        else:
            messages.error(request, 'Erro ao cadastrar iPhone. Verifique os dados e tente novamente.')
    else:
        form = iPhoneForm()
    return render(request, 'core/cadastrar_iphone.html', {'form': form})

@login_required
def estoque(request):
    iphones = iPhone.objects.filter(fornecedor=request.user)
    return render(request, 'core/estoque.html', {'iphones': iphones})

@login_required
def editar_iphone(request, pk):
    iphone = get_object_or_404(iPhone, pk=pk)
    if request.method == 'POST':
        form = iPhoneForm(request.POST, instance=iphone)
        if form.is_valid():
            form.save()
            messages.success(request, 'iPhone atualizado com sucesso.')
            return redirect('estoque')
        else:
            messages.error(request, 'Erro ao atualizar iPhone. Verifique os dados e tente novamente.')
    else:
        form = iPhoneForm(instance=iphone)
    return render(request, 'core/editar_iphone.html', {'form': form, 'iphone': iphone})

@login_required
def remover_iphone(request, pk):
    iphone = get_object_or_404(iPhone, pk=pk)
    if request.method == 'POST':
        iphone.delete()
        messages.success(request, 'iPhone removido com sucesso.')
        return redirect('estoque')
    return render(request, 'core/remover_iphone.html', {'iphone': iphone})

@login_required
def buscar_iphones(request):
    form = iPhoneSearchForm(request.GET or None)
    query = Q()
    
    if form.is_valid():
        modelo = form.cleaned_data.get('modelo')
        condicao = form.cleaned_data.get('condicao')
        memoria_interna = form.cleaned_data.get('memoria_interna')
        cor = form.cleaned_data.get('cor')
        saude_bateria = form.cleaned_data.get('saude_bateria')

        if modelo:
            query &= Q(modelo=modelo)
        if condicao:
            query &= Q(condicao=condicao)
        if memoria_interna:
            query &= Q(memoria_interna=memoria_interna)
        if cor:
            query &= Q(cor__icontains=cor)
        if saude_bateria:
            query &= Q(saude_bateria=saude_bateria)

    iphones = iPhone.objects.filter(query).exclude(fornecedor=request.user).order_by('-created_at')
    return render(request, 'core/buscar_iphones.html', {'form': form, 'iphones': iphones})

def home(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'core/home.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso.')
            return redirect('home')
        else:
            messages.error(request, 'Erro ao realizar cadastro. Verifique os dados e tente novamente.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(from_email='no-reply@example.com', request=request)
            messages.success(request, 'Email de recuperação de senha enviado.')
            return redirect('password_reset_done')
        else:
            messages.error(request, 'Erro ao enviar email de recuperação de senha.')
    else:
        form = PasswordResetForm()
    return render(request, 'core/password_reset.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

def logout_view(request):
    auth_logout(request)
    messages.success(request, 'Você saiu com sucesso.')
    return redirect('home')

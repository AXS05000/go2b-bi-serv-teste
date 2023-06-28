from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import path

from . import views
from .forms import DeleteCompForm, SelecionarFuncionarioForm
from .models import Beneficios_Mala, Funcionario
from .utils import gerar_pdf, importar_excel
from .utils2 import gerar_pdf2, importar_excel_beneficios, importar_excel_folha


@login_required(login_url='/login/')
def delete_comp_view(request):
    if request.method == 'POST':
        form = DeleteCompForm(request.POST)
        if form.is_valid():
            comp = form.cleaned_data['comp']
            Beneficios_Mala.objects.filter(comp=comp).delete()
    else:
        form = DeleteCompForm()
    return render(request, 'pdf/delete_comp.html', {'form': form})


@login_required(login_url='/login/')
def upload_excel_bene(request):
    if request.method == 'POST':
        arquivo = request.FILES['arquivo']
        importar_excel_beneficios(arquivo)
        return redirect('upload_excel_beneficio')

    return render(request, 'pdf/upload_bene.html')


@login_required(login_url='/login/')
def upload_excel_folha(request):
    if request.method == 'POST':
        arquivo = request.FILES['arquivo']
        importar_excel_folha(arquivo)
        return redirect('upload_excel_folha')

    return render(request, 'pdf/upload_folha.html')


@login_required(login_url='/login/')
def upload_excel(request):
    if request.method == 'POST':
        arquivo = request.FILES['arquivo']
        importar_excel(arquivo)
        return redirect('upload_excel')

    return render(request, 'pdf/upload.html')

@login_required(login_url='/login/')
def selecionar_funcionario(request):
    if request.method == 'POST':
        form = SelecionarFuncionarioForm(request.POST)
        if form.is_valid():
            codigo_fc = form.cleaned_data['codigo_fc']
            comp = form.cleaned_data['comp']
            try:
                funcionario = Funcionario.objects.get(codigo_fc=codigo_fc, comp=comp)
            
                return gerar_pdf(funcionario)
            except Funcionario.DoesNotExist:
                form.add_error(None, 'Funcionário não encontrado para a matrícula e competência informadas.')
    else:
        form = SelecionarFuncionarioForm()

    return render(request, 'pdf/selecionar_funcionario.html', {'form': form})


@login_required(login_url='/login/')
def selecionar_funcionario2(request):
    if request.method == 'POST':
        form = SelecionarFuncionarioForm(request.POST)
        if form.is_valid():
            codigo_fc = form.cleaned_data['codigo_fc']
            comp = form.cleaned_data['comp']
            try:
                funcionario = Funcionario.objects.get(codigo_fc=codigo_fc, comp=comp)
            
                return gerar_pdf2(funcionario)
            except Funcionario.DoesNotExist:
                form.add_error(None, 'Funcionário não encontrado para a matrícula e competência informadas.')
    else:
        form = SelecionarFuncionarioForm()

    return render(request, 'pdf/selecionar_funcionario2.html', {'form': form})


def gerar_pdf_direto(request, codigo_fc, comp):
    try:
        funcionario = Funcionario.objects.get(codigo_fc=codigo_fc, comp=comp)
        return gerar_pdf(funcionario)
    except Funcionario.DoesNotExist:
        raise Http404('Funcionário não encontrado para a matrícula e competência informadas.')
    
def gerar_pdf_direto2(request, codigo_fc, comp):
    try:
        funcionario = Funcionario.objects.get(codigo_fc=codigo_fc, comp=comp)
        return gerar_pdf2(funcionario)
    except Funcionario.DoesNotExist:
        raise Http404('Funcionário não encontrado para a matrícula e competência informadas.')

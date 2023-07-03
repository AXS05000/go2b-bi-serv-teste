import io
import os
import shutil
import tempfile

import fitz  # PyMuPDF
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import (FileResponse, Http404, HttpResponse,
                         HttpResponseRedirect)
from django.shortcuts import redirect, render
from django.urls import path

from . import views
from .forms import AutenticacaoForm, DeleteCompForm, SelecionarFuncionarioForm
from .models import Arquivo, Beneficios_Mala, Funcionario
from .tasks import (importar_excel_beneficios, importar_excel_folha_de_ponto,
                    importar_excel_funcionario)
from .utils import gerar_pdf
from .utils2 import gerar_pdf2


def find_and_extract_page(file, authentication):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    for i in range(len(doc)):
        page = doc.load_page(i)
        if authentication in page.get_text("text"):
            output = io.BytesIO()
            new_doc = fitz.open()
            new_doc.insert_pdf(doc, from_page=i, to_page=i)
            new_doc.save(output, garbage=4, deflate=True, clean=True)
            output.seek(0)
            new_doc.close()
            doc.close()
            return output
    doc.close()
    return None







def download_file(request):
    if request.method == 'POST':
        form = AutenticacaoForm(request.POST)
        if form.is_valid():
            authentication = form.cleaned_data['autenticacao']
            competencia = form.cleaned_data['competencia']
            files = Arquivo.objects.filter(competencia=competencia)
            for file_instance in files:
                file = file_instance.pdf
                extracted_file = find_and_extract_page(file, authentication)
                if extracted_file is not None:
                    return FileResponse(extracted_file, as_attachment=True, filename=authentication + '.pdf')
            return HttpResponse("Autenticação não encontrada em nenhum arquivo.")
    else:
        form = AutenticacaoForm()
    return render(request, 'download.html', {'form': form})


def download_file_url(request, competencia, autenticacao):
    files = Arquivo.objects.filter(competencia=competencia)
    for file_instance in files:
        file = file_instance.pdf
        extracted_file = find_and_extract_page(file, autenticacao)
        if extracted_file is not None:
            return FileResponse(extracted_file, as_attachment=True, filename=autenticacao + '.pdf')
    return HttpResponse("Autenticação não encontrada.")






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
        filepath = os.path.join(settings.MEDIA_ROOT, arquivo.name)

        with open(filepath, 'wb+') as destination:
            for chunk in arquivo.chunks():
                destination.write(chunk)

        importar_excel_beneficios.delay(filepath)
        return redirect('upload_excel_beneficio')

    return render(request, 'pdf/upload_bene.html')


@login_required(login_url='/login/')
def upload_excel_folha(request):
    if request.method == 'POST':
        arquivo = request.FILES['arquivo']
        filepath = os.path.join(settings.MEDIA_ROOT, arquivo.name)

        with open(filepath, 'wb+') as destination:
            for chunk in arquivo.chunks():
                destination.write(chunk)

        importar_excel_folha_de_ponto.delay(filepath)
        return redirect('upload_excel_folha')

    return render(request, 'pdf/upload_folha.html')


@login_required(login_url='/login/')
def upload_excel(request):
    if request.method == 'POST':
        arquivo = request.FILES['arquivo']
        filepath = os.path.join(settings.MEDIA_ROOT, arquivo.name)

        with open(filepath, 'wb+') as destination:
            for chunk in arquivo.chunks():
                destination.write(chunk)

        importar_excel_funcionario.delay(filepath)
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

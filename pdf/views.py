import io
import os
import re
import shutil
import tempfile

import chardet
import fitz  # PyMuPDF
import pandas as pd
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import (FileResponse, Http404, HttpResponse,
                         HttpResponseRedirect)
from django.shortcuts import redirect, render
from django.urls import path
from PyPDF2 import PdfReader, PdfWriter

from .forms import (AutenticacaoForm, CompetenciaForm, DeleteCompForm,
                    OtimizacaoForm, SelecionarFuncionarioForm, UploadExcelForm,
                    UploadFileForm)
from .models import (Arquivo, Arquivo_PDF, Beneficios_Mala, Funcionario,
                     Pagamentos)
from .tasks import (importar_excel_beneficios, importar_excel_folha_de_ponto,
                    importar_excel_funcionario)
from .utils import gerar_pdf
from .utils2 import gerar_pdf2


def busca_autenticacoes_e_gera_pdf(competencia):
    matriculas_unicas = Pagamentos.objects.filter(competencia=competencia).values_list('matricula', flat=True).distinct()
    
    for matricula in matriculas_unicas:
        pagamentos_matricula = Pagamentos.objects.filter(matricula=matricula, competencia=competencia)

        doc_output = fitz.open()  # documento de saída

        for pagamento in pagamentos_matricula:
            arquivo_referencia = pagamento.arquivo_referencia
            pagina_referencia = pagamento.pagina

            if arquivo_referencia and pagina_referencia is not None:
                doc = fitz.open(arquivo_referencia.pdf.path)
                page = doc[pagina_referencia]
                doc_output.insert_pdf(doc, from_page=pagina_referencia, to_page=pagina_referencia)

        output_filename = f"{matricula}.pdf"
        doc_output.save(output_filename)







def upload_pagamentos_mala_direta(request):
    if request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file, engine='openpyxl')  # Usar engine='xlrd' para .xls

            for index, row in df.iterrows():
                pagamento, created = Pagamentos.objects.get_or_create(
                    matricula=row['Matricula'],
                    auntenticacao=row['Autenticação'],
                    competencia=row['Competencia']
                )

            return redirect('upload_pagamentos_mala_direta')  # Substitua pelo nome da URL para onde você quer redirecionar após o upload
    else:
        form = UploadExcelForm()

    return render(request, 'pdf/upload_pagamentos_mala_direta.html', {'form': form})







def gerar_pdf_competencia(request):
    if request.method == "POST":
        form = CompetenciaForm(request.POST)
        if form.is_valid():
            busca_autenticacoes_e_gera_pdf(form.cleaned_data['competencia'])
            # Aqui, você pode decidir o que fazer após a geração dos PDFs
            return redirect('gerar_pdf_competencia') 
    else:
        form = CompetenciaForm()
    return render(request, 'pdf/pdf_mala_direta.html', {'form': form})


def indexar_autenticacoes(competencia):
    pagamentos = Pagamentos.objects.filter(competencia=competencia).exclude(auntenticacao__exact='')

    for pagamento in pagamentos:
        # Se já temos coordenadas para esta autenticação, podemos pular
        if pagamento.coordenadas_x and pagamento.coordenadas_y and pagamento.pagina is not None:
            continue

        autenticacao_encontrada = False

        for arquivo in Arquivo.objects.filter(competencia=competencia):
            doc = fitz.open(arquivo.pdf.path)

            for page_num, page in enumerate(doc):
                areas = page.search_for(pagamento.auntenticacao)
                if areas:
                    rect = areas[0]  # Pegando a primeira ocorrência da autenticação na página
                    pagamento.coordenadas_x = rect.x0
                    pagamento.coordenadas_y = rect.y0
                    pagamento.arquivo_referencia = arquivo
                    pagamento.pagina = page_num  # Salvando o número da página
                    pagamento.save()
                    autenticacao_encontrada = True
                    break

            if autenticacao_encontrada:
                break






def otimizar_referencias(request):
    if request.method == "POST":
        form = OtimizacaoForm(request.POST)
        if form.is_valid():
            indexar_autenticacoes(form.cleaned_data['competencia'])
            return redirect('otimizar') 
    else:
        form = OtimizacaoForm()
    return render(request, 'pdf/template_otimizacao.html', {'form': form})




















def extract_info_from_page(page):
    text = page.get_text("text")

    # Use expressões regulares para extrair as informações
    cpf_cnpj = re.findall(r"CPF/CNPJ:\s*([\d.-]+)", text)
    data_pagamento = re.findall(r"DATA (?:DO PAGAMENTO|DA TRANSFERENCIA):\s*([\d/]+)", text)
    valor = re.findall(r"VALOR:\s*([\d.,]+)", text)
    nr_autenticacao = re.findall(r"NR. AUTENTICACAO:\s*([.\d\w]+)", text)

    # Certifique-se de que as listas não estejam vazias antes de pegar o primeiro elemento
    cpf_cnpj = cpf_cnpj[0] if cpf_cnpj else ''
    data_pagamento = data_pagamento[0] if data_pagamento else ''
    valor = valor[0] if valor else ''
    nr_autenticacao = nr_autenticacao[0] if nr_autenticacao else ''

    return cpf_cnpj, data_pagamento, valor, nr_autenticacao


def find_and_extract_page_para_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    all_info = []
    for i in range(len(doc)):
        page = doc.load_page(i)
        info = extract_info_from_page(page)
        all_info.append(info)
    doc.close()
    return all_info





def upload_file_banco_pdf(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = Arquivo_PDF(pdf=request.FILES['file'])
            new_file.save()

            all_info = find_and_extract_page_para_pdf(new_file.pdf)
            
            # Transforme as informações coletadas em um DataFrame pandas
            df = pd.DataFrame(all_info, columns=["CPF/CNPJ", "Data do Pagamento", "Valor", "Nr. Autenticacao"])
            
            # Obtenha apenas o nome do arquivo, sem o diretório
            filename = os.path.basename(new_file.pdf.name)
            
            # Crie um diretório para os arquivos .xlsx se ele não existir
            os.makedirs('xlsx_files', exist_ok=True)
            
            # Escreva o DataFrame em um arquivo Excel
            df.to_excel("xlsx_files/Informações_extraídas_" + filename + ".xlsx")

            return redirect('upload_banco_pdf')
    else:
        form = UploadFileForm()
    return render(request, 'notas/upload_pdf_banco.html', {'form': form})
























def extracao_retorno_bradesco(file):
    # Detecta a codificação do arquivo
    rawdata = file.read()
    result = chardet.detect(rawdata)
    encoding = result['encoding']

    # Lê o arquivo linha por linha usando a codificação detectada
    lines = rawdata.decode(encoding).splitlines()

    data = []
    for i in range(2, len(lines)-2):  # Ignora as duas primeiras e duas últimas linhas
        if lines[i][13] == 'A':
            re_fc = lines[i][79:85] + lines[i][76:79]
            re_gi = lines[i][79:85]
            data_baixa = lines[i][93:101]
            valor_pago = lines[i][169:177]
        elif lines[i][13] == 'B':
            autenticacao = lines[i+1][78:103] if lines[i+1][13] == 'Z' else None  # Certifique-se de que esses índices estão corretos
            data.append({
                'autenticacao': autenticacao,
                're_fc': re_fc,
                're_gi': re_gi,
                'data_baixa': data_baixa,
                'valor_pago': valor_pago
            })
    df = pd.DataFrame(data)
    return df


def process_local_folder_bradesco(folder_path):
    # Percorre todas as subpastas da pasta fornecida
    for root, dirs, files in os.walk(folder_path):
        # Processa cada arquivo .ret
        for filename in files:
            if filename.endswith('.ret'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'rb') as file:
                    df = extracao_retorno_bradesco(file)

                # Salva o DataFrame como um arquivo Excel na mesma pasta
                df.to_excel(filepath.replace('.ret', '.xlsx'), index=False)


def process_files_view_bradesco(request):
    process_local_folder_bradesco(r"C:\Users\Alex Sobreira\Desktop\TRABALHADO AUTENTICAÇÕES\TRATATIVA AGOSTO SEM AUTENTICAÇÃO\BRADESCO")
    return HttpResponse("Arquivos processados com sucesso")




















def extracao_retorno_itau(file):
    # Detecta a codificação do arquivo
    rawdata = file.read()
    result = chardet.detect(rawdata)
    encoding = result['encoding']

    # Lê o arquivo linha por linha usando a codificação detectada
    lines = rawdata.decode(encoding).splitlines()

    data = []
    for i in range(2, len(lines)-2):  # Ignora as duas primeiras e duas últimas linhas
        if lines[i][13] == 'A':
            cpf = lines[i][206:217]
            data_baixa = lines[i][93:101]
            valor_pago = lines[i][169:177]
            autenticacao = lines[i+1][14:85]  + '-CTRL: ' +lines[i+1][103:118] if lines[i+1][13] == 'Z' else None  # Certifique-se de que esses índices estão corretos
            data.append({
                'cpf': cpf,
                'autenticacao': autenticacao,
                'data_baixa': data_baixa,
                'valor_pago': valor_pago
            })
    df = pd.DataFrame(data)
    return df



def process_local_folder_itau(folder_path):
    print(f"Processing folder: {folder_path}")
    # Percorre todas as subpastas da pasta fornecida
    for root, dirs, files in os.walk(folder_path):
        print(f"Found {len(files)} files in {root}")
        # Processa cada arquivo .RET
        for filename in files:
            print(f"Processing file: {filename}")
            if filename.lower().endswith('.ret'):  # Agora isso verificará tanto '.RET' quanto '.ret'
                filepath = os.path.join(root, filename)
                print(f"Processing RET file: {filepath}")
                with open(filepath, 'rb') as file:
                    df = extracao_retorno_itau(file)

                # Salva o DataFrame como um arquivo Excel na mesma pasta
                excel_path = filepath.replace('.ret', '.xlsx').replace('.RET', '.xlsx')
                print(f"Saving DataFrame to Excel file: {excel_path}")
                df.to_excel(excel_path, index=False)
                print(f"Saved Excel file: {excel_path}")




def process_files_view_itau(request):
    process_local_folder_itau(r"C:\Users\Alex Sobreira\Desktop\TRABALHADO AUTENTICAÇÕES\TRATATIVA AGOSTO SEM AUTENTICAÇÃO\ITAU")
    return HttpResponse("Arquivos processados com sucesso")








def upload_file_bet_itau(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            df = extracao_retorno_itau(request.FILES['file'])

            # Escreve o DataFrame em um arquivo Excel
            excel_file = io.BytesIO()
            with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Funcionarios', index=False)
            excel_file.seek(0)

            # Configura a resposta para fazer o download do arquivo Excel
            response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=funcionarios.xlsx'

            return response
    else:
        form = UploadFileForm()
    return render(request, 'pdf/gerar_excel_banco2.html', {'form': form})










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


def download_file_url(request, competencia, autenticacao):
    files = Arquivo.objects.filter(competencia=competencia)
    for file_instance in files:
        file = file_instance.pdf
        extracted_file = find_and_extract_page(file, autenticacao)
        if extracted_file is not None:
            return FileResponse(extracted_file, as_attachment=True, filename=autenticacao + '.pdf')
    return HttpResponse("Autenticação não encontrada.")




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













########################## EXTRAÇÃO DO ARQUIVO DE RETORNO BB################################################


def upload_file_bet(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = handle_uploaded_file2(request.FILES['file'])

            # Configura a resposta para fazer o download do arquivo Excel
            response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=funcionarios.xlsx'

            return response
    else:
        form = UploadFileForm()
    return render(request, 'pdf/gerar_excel_banco.html', {'form': form})



def handle_uploaded_file2(file):
    # Lê o arquivo linha por linha
    lines = file.read().decode('utf-8').splitlines()

    data = []
    for i in range(2, len(lines)-2):  # Ignora as duas primeiras e duas últimas linhas
        if lines[i][13] == 'A':
            re_fc = lines[i][86:92] + lines[i][76:79]
            re_gi = lines[i][86:92]
            cliente_gi = lines[i][79:85]
            data_baixa = lines[i][93:101]
            valor_pago = lines[i][169:177]
        elif lines[i][13] == 'B':
            cpf = lines[i][21:32]  # Certifique-se de que esses índices estão corretos
            autenticacao = lines[i+1][78:94] if lines[i+1][13] == 'Z' else None  # Certifique-se de que esses índices estão corretos
            data.append({
                'cpf': cpf, 
                'autenticacao': autenticacao,
                're_fc': re_fc,
                're_gi': re_gi,
                'cliente_gi': cliente_gi,
                'data_baixa': data_baixa,
                'valor_pago': valor_pago
            })

    # Converte a lista de dicionários em DataFrame
    df = pd.DataFrame(data)

    # Escreve o DataFrame em Excel
    excel_file = io.BytesIO()
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Funcionarios', index=False)
    excel_file.seek(0)

    return excel_file


#######################################PARTE DESKTOP##############################################################

def handle_uploaded_file(file):
    # Detecta a codificação do arquivo
    rawdata = file.read()
    result = chardet.detect(rawdata)
    encoding = result['encoding']

    # Lê o arquivo linha por linha usando a codificação detectada
    lines = rawdata.decode(encoding).splitlines()

    data = []
    for i in range(2, len(lines)-2):  # Ignora as duas primeiras e duas últimas linhas
        if lines[i][13] == 'A':
            re_fc = lines[i][86:92] + lines[i][76:79]
            re_gi = lines[i][86:92]
            cliente_gi = lines[i][79:85]
            data_baixa = lines[i][93:101]
            valor_pago = lines[i][169:177]
        elif lines[i][13] == 'B':
            cpf = lines[i][21:32]  # Certifique-se de que esses índices estão corretos
            autenticacao = lines[i+1][78:94] if lines[i+1][13] == 'Z' else None  # Certifique-se de que esses índices estão corretos
            data.append({
                'cpf': cpf, 
                'autenticacao': autenticacao,
                're_fc': re_fc,
                're_gi': re_gi,
                'cliente_gi': cliente_gi,
                'data_baixa': data_baixa,
                'valor_pago': valor_pago
            })
    df = pd.DataFrame(data)
    return df




def process_local_folder(folder_path):
    # Percorre todas as subpastas da pasta fornecida
    for root, dirs, files in os.walk(folder_path):
        # Processa cada arquivo .ret
        for filename in files:
            if filename.endswith('.ret'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'rb') as file:
                    df = handle_uploaded_file(file)

                # Salva o DataFrame como um arquivo Excel na mesma pasta
                df.to_excel(filepath.replace('.ret', '.xlsx'), index=False)


def process_files_view(request):
    process_local_folder(r"C:\Users\Alex Sobreira\Desktop\TRABALHADO AUTENTICAÇÕES\TRATATIVA AGOSTO SEM AUTENTICAÇÃO\BB")
    return HttpResponse("Arquivos processados com sucesso")


###############################################################################################################################
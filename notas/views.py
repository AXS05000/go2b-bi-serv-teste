import csv
import re
from datetime import date, datetime, timedelta
from decimal import Decimal

from django.contrib import messages
from django.core.paginator import PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseRedirect
# from core.main import make_recipe - Importação para testar as coisas.
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView
from zeep import Client

from .forms import BaseCNPJModelForm, NotasModelForm
from .models import BaseCNPJ, NotaFiscal2, Notas, NumeradorLote
from .utils import import_basecnpj_from_excel, update_basecnpj_from_excel

#########################################################################################


# BUSCA E GERAÇÃO DO TXT
class Notas_FiscaisView(ListView):
    model = NotaFiscal2
    template_name = 'notas/notas_portal.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['order_by'] = self.request.GET.get('order_by', '-numero')
        page_obj = context['page_obj']

        # Obtém o número da página atual
        current_page = page_obj.number

        # Se há mais de 5 páginas
        if page_obj.paginator.num_pages > 5:
            if current_page - 2 < 1:
                start_page = 1
                end_page = 5
            elif current_page + 2 > page_obj.paginator.num_pages:
                start_page = page_obj.paginator.num_pages - 4
                end_page = page_obj.paginator.num_pages
            else:
                start_page = current_page - 2
                end_page = current_page + 2
        else:
            start_page = 1
            end_page = page_obj.paginator.num_pages

        context['page_range'] = range(start_page, end_page + 1)

        return context



    def get_queryset(self):
        query = self.request.GET.get('q')
        order_by = self.request.GET.get('order_by', '-numero')
        if query:
            try:
                date_query = datetime.strptime(query, '%d/%m/%Y').date()  
                return NotaFiscal2.objects.filter(Q(data_emissao=date_query)).order_by(order_by)
            except ValueError:
                notas_by_cnpj = NotaFiscal2.objects.filter(doc_tomador__icontains=query).order_by(order_by)
                notas_by_nome_cliente = NotaFiscal2.objects.filter(nome_tomador__icontains=query).order_by(order_by)
                return (notas_by_cnpj | notas_by_nome_cliente)
        return NotaFiscal2.objects.all().order_by(order_by)


class GerarcsvTemplateView(ListView):
    model = Notas
    template_name = 'notas/notas_do_sistema.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['order_by'] = self.request.GET.get('order_by', '-data_de_criacao')
        page_obj = context['page_obj']

        # Obtém o número da página atual
        current_page = page_obj.number

        # Se há mais de 5 páginas
        if page_obj.paginator.num_pages > 5:
            if current_page - 2 < 1:
                start_page = 1
                end_page = 5
            elif current_page + 2 > page_obj.paginator.num_pages:
                start_page = page_obj.paginator.num_pages - 4
                end_page = page_obj.paginator.num_pages
            else:
                start_page = current_page - 2
                end_page = current_page + 2
        else:
            start_page = 1
            end_page = page_obj.paginator.num_pages

        context['page_range'] = range(start_page, end_page + 1)

        return context



    def get_queryset(self):
        query = self.request.GET.get('q')
        order_by = self.request.GET.get('order_by', '-data_de_criacao')
        if query:
            try:
                date_query = datetime.strptime(query, '%d/%m/%Y').date()  # Ajustando o formato aqui
                return Notas.objects.filter(Q(data_de_criacao=date_query)).order_by(order_by)
            except ValueError:  # Captura a exceção se a data for inválida
                # Aqui você pode lidar com a situação onde a data é inválida, por exemplo, verificando se 'q' corresponde a uma unidade ou nome de cliente
                notas_by_unidade = Notas.objects.filter(cnpj_da_nota__unidade__icontains=query).order_by(order_by)
                notas_by_nome_cliente = Notas.objects.filter(cnpj_da_nota__nome_cliente__icontains=query).order_by(order_by)
                return (notas_by_unidade | notas_by_nome_cliente)  # Retorna a união dos dois conjuntos de notas
        return Notas.objects.all().order_by(order_by)
    


# PUXAR NOTAS PARA O MODELS.
def atualizar_notas(request):
    if request.method == 'POST':
        response = consultar_api()

        if not response['Erro']:
            notas_geradas = response['NotasGeradas']['NotaFiscalConsultaDTO']
            NotaFiscal2.objects.all().delete()  # Remove as notas existentes

            for nota in notas_geradas:
                NotaFiscal2.objects.create(
                    aliquota = nota['Aliquota'],
                    cod_atividade = nota['CodAtividade'].strip(),
                    cod_obra = nota['CodObra'],
                    codigo_autenticidade = nota['CodigoAutenticidade'],
                    data_cancelamento = nota['DataCancelamento'],
                    data_emissao = nota['DataEmissao'],
                    data_recibo = nota['DataRecibo'],
                    doc_tomador = nota['DocTomador'],
                    endereco_prestacao_servico = nota['EnderecoPrestacaoServico'],
                    link_nfe = nota['LinkNFE'],
                    motivo_cancelamento = nota['MotivoCancelamento'],
                    nome_tomador = nota['NomeTomador'],
                    nosso_numero = nota['NossoNumero'],
                    numero = nota['Numero'],
                    numero_recibo = nota['NumeroRecibo'],
                    substituicao_tributaria = nota['SubstituicaoTributaria'],
                    valor = nota['Valor'],
                    valor_iss = nota['ValorIss'],
                    valor_nfe = nota['ValorNFE']
                )

            return render(request, 'notas/update.html', {'notas': NotaFiscal2.objects.all()})
        else:
            print(f"Erro: {response['MensagemErro']}")

    return render(request, 'notas/update.html')


def atualizar_notas_automaticamente():
    response = consultar_api()

    if not response['Erro']:
        notas_geradas = response['NotasGeradas']['NotaFiscalConsultaDTO']
        NotaFiscal2.objects.all().delete()  # Remove as notas existentes

        for nota in notas_geradas:
                NotaFiscal2.objects.create(
                    aliquota = nota['Aliquota'],
                    cod_atividade = nota['CodAtividade'].strip(),
                    cod_obra = nota['CodObra'],
                    codigo_autenticidade = nota['CodigoAutenticidade'],
                    data_cancelamento = nota['DataCancelamento'],
                    data_emissao = nota['DataEmissao'],
                    data_recibo = nota['DataRecibo'],
                    doc_tomador = nota['DocTomador'],
                    endereco_prestacao_servico = nota['EnderecoPrestacaoServico'],
                    link_nfe = nota['LinkNFE'],
                    motivo_cancelamento = nota['MotivoCancelamento'],
                    nome_tomador = nota['NomeTomador'],
                    nosso_numero = nota['NossoNumero'],
                    numero = nota['Numero'],
                    numero_recibo = nota['NumeroRecibo'],
                    substituicao_tributaria = nota['SubstituicaoTributaria'],
                    valor = nota['Valor'],
                    valor_iss = nota['ValorIss'],
                    valor_nfe = nota['ValorNFE']
                )

        print("Notas atualizadas com sucesso.")
    else:
        print(f"Erro: {response['MensagemErro']}")
























########################################GERAÇÃO DO TXT##############################################
def preenche_zeros(string, total_chars):
    return str(string).zfill(total_chars)

def preenche_espacos(string, total_chars):
    return str(string).ljust(total_chars)

def format_date(date):
    return date.strftime("%d%m%Y")

def add_days(date, days):
    return format_date(date + timedelta(days=days))

def generate_txt(request):
    selected_notas = request.POST.getlist('notas')
    if selected_notas:
        notas = NotaFiscal2.objects.filter(id__in=selected_notas)
    else:
        notas = NotaFiscal2.objects.all()


    
    current_datetime = timezone.now()
    file_date = format_date(current_datetime)
    file_hour = current_datetime.strftime("%H%M%S")

    numerador_lote = NumeradorLote.objects.first()
    if numerador_lote is None: 
        numerador_lote = NumeradorLote(valor=1)
    else:
        numerador_lote.valor += 1
    numerador_lote.save()
    
    lote_seq = preenche_zeros(numerador_lote.valor, 6)
    lote_seq2 = preenche_zeros(numerador_lote.valor, 2)

    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="LOTE {lote_seq2}.txt"'
    
    header = f'24600000         218504752000155CC019070022370680000CC019070022370680000GOIASBUSINESSCONSULTESERVLTDA BCO ABC BRASIL                          1{file_date}{file_hour}{lote_seq}04001600                                                                     \n'
    response.write(header)
    
    second_line = f'24600011R01  030 2018504752000155CC019070022370680000CC019070022370680000GOIASBUSINESSCONSULTESERVLTDA                                                                                 00{lote_seq}{file_date}000000                                   \n'
    response.write(second_line)

    total_lines = 2
    total_notas = 0
    total_value = 0

    for nota in notas:
        total_notas += 1
        total_value += nota.valor
        line_seq = preenche_zeros(total_notas, 5)
        nota_num = preenche_espacos(nota.numero, 15)
        date_90_days = add_days(current_datetime, 90)
        nota_val = preenche_zeros(int(round(nota.valor, 2)*100), 15)
        nota_date = format_date(nota.data_emissao)
        
        nota_line1 = f'24600013{line_seq}P 01CC0190700223706800005000001000000000000011211{nota_num}{date_90_days}{nota_val}00000902N{nota_date}300000000000000000000000000000000000000000000000000000000000000000000000000000                         30020000900000000000\n'
        response.write(nota_line1)

        total_notas += 1
        line_seq = preenche_zeros(total_notas, 5)
        
        nota_line2 = f'24600013{line_seq}Q 012003502099000118CHUBBSEGUROSBRASILSA                    Avenida OLIVEIRA PAIVA 2800             Pinheiros      05402920SaoPaulo       SP0000000000000000                                        000                            \n'
        response.write(nota_line2)

        total_lines += 2

    total_value_str = preenche_zeros(int(round(total_value, 2)*100), 17)
    total_lines_str = preenche_zeros(total_lines, 6)
    total_lines_str2 = preenche_zeros(int(total_lines-2), 6)
    total_notas_str = preenche_zeros(int((total_lines-2)/2), 6)


    trailler1 = f'24600015         {total_lines_str}00000000000000000000000{total_notas_str}{total_value_str}0000000000000000000000000000000000000000000000                                                                                                                             \n'
    response.write(trailler1) 

    trailler2 = f'24699999         000001{total_lines_str2}                                                                                                                                                                                                                   \n'
    response.write(trailler2) 

    return response


#CONSULTA NA API
def consultar_api():
    # Criando o objeto cliente SOAP
    client = Client('https://nfe.osasco.sp.gov.br/EISSNFEWebServices/NotaFiscalEletronica.svc?wsdl')

    # Criando o request com os dados passados
    request_data = {
        'ChaveAutenticacao': '5eb04d8c-fd9a-49ba-ab45-d06d816df7ad',  # valor fixo
        'DataInicial': date(2023, 5, 1),  # valor fixo
        'DataFinal': date.today(),  # data de hoje
        'NumeroReciboInicial': None,  # valor fixo
        'NumeroReciboFinal': None,  # valor fixo
        'NumeroReciboUnico': None  # valor fixo
    }

    # Fazendo a requisição e obtendo a resposta
    response = client.service.Consultar(request=request_data)

    # Retornando a resposta
    return response


# BUSCAR NOTAS (BACKUP)
def buscar_notas(request):
    wsdl = 'https://nfe.osasco.sp.gov.br/EISSNFEWebServices/NotaFiscalEletronica.svc?wsdl'
    client = Client(wsdl)
    response = None

    if request.method == 'POST':
        request_data = {
            'ChaveAutenticacao': '5eb04d8c-fd9a-49ba-ab45-d06d816df7ad',
        }

        # Se os campos de data estiverem presentes, adicione-os à solicitação
        data_inicial = request.POST.get('data_inicial', None)
        data_final = request.POST.get('data_final', None)
        if data_inicial and data_final:
            request_data['DataInicial'] = data_inicial
            request_data['DataFinal'] = data_final

        # Se os campos de número de recibo estiverem presentes, adicione-os à solicitação
        numero_recibo_inicial = request.POST.get('numero_recibo_inicial', None)  # opcional
        numero_recibo_final = request.POST.get('numero_recibo_final', None)  # opcional
        if numero_recibo_inicial and numero_recibo_final:
            # Converte para int antes de adicionar à solicitação
            request_data['NumeroReciboInicial'] = int(numero_recibo_inicial)
            request_data['NumeroReciboFinal'] = int(numero_recibo_final)

        # Se o campo de número de recibo único estiver presente, adicione-o à solicitação
        numero_recibo_unico = request.POST.get('numero_recibo_unico', None)  # opcional
        if numero_recibo_unico:
            # Converte para int antes de adicionar à solicitação
            request_data['NumeroReciboUnico'] = int(numero_recibo_unico)

        response = client.service.Consultar(request = request_data)


    return render(request, 'notas/buscar_notas_portal.html', {'response': response})
###################################################################################################################





###################################NOTAS VERSÃO ANTIGA######################################################


def qtddecargos(request):
    return render(request, 'qtddecargos.html')


class NotaFiscalCreateView(CreateView):
    model = Notas
    form_class = NotasModelForm
    template_name = 'notas/notafiscal.html'
    success_url = '/notafiscal/'

    def form_valid(self, form):
        messages.success(self.request, 'Nota salva com sucesso.')
        return super().form_valid(form)
    
    

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao salvar o formulário, por favor verifique as informações preenchidas.')
        return super().form_invalid(form)




# 2 Cargos

def notafiscal2(request):
    if str(request.method) == 'POST':
        form = NotasModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Formulario salvo com sucesso')
            form = NotasModelForm()
        else:
            messages.error(request, 'Erro ao salvar o formulario')
            
    else:
        form = NotasModelForm()
    context = {
        'form': form
    }
    return render(request, 'notafiscal2.html', context)

# 3 Cargos

def notafiscal3(request):
    if str(request.method) == 'POST':
        form = NotasModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Formulario salvo com sucesso')
            form = NotasModelForm()
        else:
            messages.error(request, 'Erro ao salvar o formulario')
            
    else:
        form = NotasModelForm()
    context = {
        'form': form
    }
    return render(request, 'notafiscal3.html', context)


# 4 Cargos

def notafiscal4(request):
    if str(request.method) == 'POST':
        form = NotasModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Formulario salvo com sucesso')
            form = NotasModelForm()
        else:
            messages.error(request, 'Erro ao salvar o formulario')
            
    else:
        form = NotasModelForm()
    context = {
        'form': form
    }
    return render(request, 'notafiscal4.html', context)

# 5 Cargos

def notafiscal5(request):
    if str(request.method) == 'POST':
        form = NotasModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Formulario salvo com sucesso')
            form = NotasModelForm()
        else:
            messages.error(request, 'Erro ao salvar o formulario')
            
    else:
        form = NotasModelForm()
    context = {
        'form': form
    }
    return render(request, 'notafiscal5.html', context)

# 6 Cargos

def notafiscal6(request):
    if str(request.method) == 'POST':
        form = NotasModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Formulario salvo com sucesso')
            form = NotasModelForm()
        else:
            messages.error(request, 'Erro ao salvar o formulario')
            
    else:
        form = NotasModelForm()
    context = {
        'form': form
    }
    return render(request, 'notafiscal6.html', context)


# 7 Cargos

def notafiscal7(request):
    if str(request.method) == 'POST':
        form = NotasModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Formulario salvo com sucesso')
            form = NotasModelForm()
        else:
            messages.error(request, 'Erro ao salvar o formulario')
            
    else:
        form = NotasModelForm()
    context = {
        'form': form
    }
    return render(request, 'notafiscal7.html', context)

# 8 Cargos

def notafiscal8(request):
    if str(request.method) == 'POST':
        form = NotasModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Formulario salvo com sucesso')
            form = NotasModelForm()
        else:
            messages.error(request, 'Erro ao salvar o formulario')
            
    else:
        form = NotasModelForm()
    context = {
        'form': form
    }
    return render(request, 'notafiscal8.html', context)


def cnpj(request):
    if str(request.method) == 'POST':
        form = BaseCNPJModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Formulario salvo com sucesso')
            form = BaseCNPJModelForm()
        else:
            messages.error(request, 'Erro ao salvar o formulario')
            
    else:
        form = BaseCNPJModelForm()
    context = {
        'form': form
    }
    return render(request, 'cnpj.html', context)



def fatoutros(request):
    if str(request.method) == 'POST':
        form = NotasModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Formulario salvo com sucesso')
            form = NotasModelForm()
        else:
            messages.error(request, 'Erro ao salvar o formulario')
            
    else:
        form = NotasModelForm()
    context = {
        'form': form
    }
    return render(request, 'fatoutros.html', context)








def update_basecnpj(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        update_basecnpj_from_excel(excel_file)
        return render(request, 'atualizar_cnpj.html', {'success': True})
    return render(request, 'atualizar_cnpj.html')

def import_basecnpj(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        import_basecnpj_from_excel(excel_file)
        return render(request, 'import_basecnpj.html', {'success': True})
    return render(request, 'import_basecnpj.html')





####################################################################################















































###############################################################################


#GERAR CSV PARA IMPORTAÇÃO DAS NOTAS
def generate_csv(request):
    selected_notas = request.POST.getlist('notas')
    if selected_notas:
        notas = Notas.objects.filter(id__in=selected_notas)
    else:
        notas = Notas.objects.all()
    notas = Notas.objects.filter(id__in=selected_notas)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="notas.csv"'

    writer = csv.writer(response, delimiter=';')
    today = timezone.now().strftime("%Y-%m-%d")
    test_marker = 'T' if 'test' in request.GET else ''
    first_row = ['H', today, today, test_marker, '18504752000155']
    writer.writerow(first_row)

    def generate_description(nota):
        descricao = ""
        if nota.porcentagem_ans is not None and nota.total_valor_outros is None:
            total_a_faturar_nota = round(nota.total_a_faturar - (nota.total_a_faturar * nota.porcentagem_ans) , 4)

        elif nota.porcentagem_ans is None and nota.total_valor_outros is not None:
            total_a_faturar_nota = round(nota.total_valor_outros, 4)

        else:
            total_a_faturar_nota = round(nota.total_a_faturar, 4) 

        base_pis = total_a_faturar_nota * Decimal("0.0065")
        base_confins = total_a_faturar_nota * Decimal("0.03")
        base_inss = total_a_faturar_nota * Decimal("0.11")
        base_ir = total_a_faturar_nota * Decimal("0.048")
        base_cssl = total_a_faturar_nota * Decimal("0.01")
        base_iss = total_a_faturar_nota * nota.cnpj_da_nota.iss
        total_liquido_descricao = round(total_a_faturar_nota - (base_pis + base_confins + base_inss + base_ir + base_cssl + base_iss) , 4)



        if nota.tipo_de_faturamento == 'FATURAMENTO HORAS' and nota.cnpj_da_nota.tipo_de_cliente == 'LOG' and nota.porcentagem_ans is None:
            descricao = f"PRESTAÇÃO DE SERVIÇOS DE APOIO A OPERAÇÃO DE ARMAZENAGEM E LOGISTICA|\n\nCONTRATO: {nota.baseinfocontratos.contrato} - COMPETÊNCIA: {nota.competencia_nota}|\n\n"
            for baseinfocontratos_field, quantidade_hora_field in [('baseinfocontratos', 'quantidade_hora'), ('baseinfocontratos2', 'quantidade_hora2'), ('baseinfocontratos3', 'quantidade_hora3'), ('baseinfocontratos4', 'quantidade_hora4'), ('baseinfocontratos5', 'quantidade_hora5'), ('baseinfocontratos6', 'quantidade_hora6'), ('baseinfocontratos7', 'quantidade_hora7'), ('baseinfocontratos8', 'quantidade_hora8')]:  # adicione aqui todos os pares baseinfocontratos/quantidade_hora
                baseinfocontratos = getattr(nota, baseinfocontratos_field)
                quantidade_hora = getattr(nota, quantidade_hora_field)
                if baseinfocontratos and quantidade_hora:
                    total_bruto_cargo = round(baseinfocontratos.valor_hora * Decimal(str(quantidade_hora)), 4)
                    total_bruto_cargo = str(total_bruto_cargo).replace('.', ',')  # substitui o ponto por vírgula
                    descricao += f"CARGO: {baseinfocontratos.cargo} - QTD HS: {quantidade_hora}- VALOR HORA: R${baseinfocontratos.valor_hora} TOTAL BRUTO CARGO: R$ {total_bruto_cargo}|\n\n"
            descricao += f"||TOTAL A FATURAR: R$ {format(total_a_faturar_nota, '.4f').replace('.', ',')}|\n\n BASE PARA RETENÇÕES:|\n\nRETENÇÃO CONFORME LEI 10833/03 - PIS: 0,0065: R$ {format(base_pis, '.4f').replace('.', ',')}|\n\nRETENÇÃO CONFORME LEI 10833/03 - CONFINS: 0,03: R$ {format(base_confins, '.4f').replace('.', ',')}|\n\n INSS RETENÇÃO: 0,11: R$ {format(base_inss, '.4f').replace('.', ',')}|\n\n I.R. RETENÇÃO: 0,048: R$ {format(base_ir, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 10833/03 - CSLL: 0,01: R$ {format(base_cssl, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 116/03 - ISS: {format(base_iss, '.4f').replace('.', ',')}|\n\n TOTAL LIQUIDO A RECEBER: R$ {format(total_liquido_descricao, '.4f').replace('.', ',')}|"


        if nota.tipo_de_faturamento == 'FATURAMENTO HORAS' and nota.cnpj_da_nota.tipo_de_cliente == 'MOT' and nota.porcentagem_ans is None:
            descricao = f"PRESTAÇÃO DE SERVIÇOS DE APOIO A OPERAÇÃO DE ARMAZENAGEM E LOGISTICA|\n\nCONTRATO: {nota.baseinfocontratos.contrato} - COMPETÊNCIA: {nota.competencia_nota}|\n\n"
            for baseinfocontratos_field, quantidade_hora_field in [('baseinfocontratos', 'quantidade_hora'), ('baseinfocontratos2', 'quantidade_hora2'), ('baseinfocontratos3', 'quantidade_hora3'), ('baseinfocontratos4', 'quantidade_hora4'), ('baseinfocontratos5', 'quantidade_hora5'), ('baseinfocontratos6', 'quantidade_hora6'), ('baseinfocontratos7', 'quantidade_hora7'), ('baseinfocontratos8', 'quantidade_hora8')]:  # adicione aqui todos os pares baseinfocontratos/quantidade_hora
                baseinfocontratos = getattr(nota, baseinfocontratos_field)
                quantidade_hora = getattr(nota, quantidade_hora_field)
                if baseinfocontratos and quantidade_hora:
                    total_bruto_cargo = round(baseinfocontratos.valor_hora * Decimal(str(quantidade_hora)), 4)
                    total_bruto_cargo = str(total_bruto_cargo).replace('.', ',')  # substitui o ponto por vírgula
                    descricao += f"CARGO: {baseinfocontratos.cargo} - QTD HS: {quantidade_hora}- VALOR HORA: R${baseinfocontratos.valor_hora} TOTAL BRUTO CARGO: R$ {total_bruto_cargo}|\n\n"
            descricao += f"||TOTAL A FATURAR: R$ {format(total_a_faturar_nota, '.4f').replace('.', ',')}|\n\n BASE PARA RETENÇÕES:|\n\nRETENÇÃO CONFORME LEI 10833/03 - PIS: 0,0065: R$ {format(base_pis, '.4f').replace('.', ',')}|\n\nRETENÇÃO CONFORME LEI 10833/03 - CONFINS: 0,03: R$ {format(base_confins, '.4f').replace('.', ',')}|\n\n INSS RETENÇÃO: 0,11: R$ {format(base_inss, '.4f').replace('.', ',')}|\n\n I.R. RETENÇÃO: 0,048: R$ {format(base_ir, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 10833/03 - CSLL: 0,01: R$ {format(base_cssl, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 116/03 - ISS: {format(base_iss, '.4f').replace('.', ',')}|\n\n TOTAL LIQUIDO A RECEBER: R$ {format(total_liquido_descricao, '.4f').replace('.', ',')}|"


        if nota.tipo_de_faturamento == 'FATURAMENTO HORAS' and nota.cnpj_da_nota.tipo_de_cliente == 'DISTRIBUIÇÃO' and nota.porcentagem_ans is None:
            descricao = f"PRESTAÇÃO DE SERVIÇOS CONTINUADOS DE APOIO AS UNIDADE DE DISTRUIBUIÇÃO, UNIDADE: {nota.cnpj_da_nota.unidade} MCU: {nota.cnpj_da_nota.mcu}|\n\nCONTRATO: {nota.baseinfocontratos.contrato} - COMPETÊNCIA: {nota.competencia_nota}|\n\n"
            for baseinfocontratos_field, quantidade_hora_field in [('baseinfocontratos', 'quantidade_hora'), ('baseinfocontratos2', 'quantidade_hora2'), ('baseinfocontratos3', 'quantidade_hora3'), ('baseinfocontratos4', 'quantidade_hora4'), ('baseinfocontratos5', 'quantidade_hora5'), ('baseinfocontratos6', 'quantidade_hora6'), ('baseinfocontratos7', 'quantidade_hora7'), ('baseinfocontratos8', 'quantidade_hora8')]:  # adicione aqui todos os pares baseinfocontratos/quantidade_hora
                baseinfocontratos = getattr(nota, baseinfocontratos_field)
                quantidade_hora = getattr(nota, quantidade_hora_field)
                if baseinfocontratos and quantidade_hora:
                    total_bruto_cargo = round(baseinfocontratos.valor_hora * Decimal(str(quantidade_hora)), 4)
                    total_bruto_cargo = str(total_bruto_cargo).replace('.', ',')  # substitui o ponto por vírgula
                    descricao += f"CARGO: {baseinfocontratos.cargo} - QTD HS: {quantidade_hora}- VALOR HORA: R${baseinfocontratos.valor_hora} TOTAL BRUTO CARGO: R$ {total_bruto_cargo}|\n\n"
            descricao += f"||TOTAL A FATURAR: R$ {format(total_a_faturar_nota, '.4f').replace('.', ',')}|\n\n BASE PARA RETENÇÕES:|\n\nRETENÇÃO CONFORME LEI 10833/03 - PIS: 0,0065: R$ {format(base_pis, '.4f').replace('.', ',')}|\n\nRETENÇÃO CONFORME LEI 10833/03 - CONFINS: 0,03: R$ {format(base_confins, '.4f').replace('.', ',')}|\n\n INSS RETENÇÃO: 0,11: R$ {format(base_inss, '.4f').replace('.', ',')}|\n\n I.R. RETENÇÃO: 0,048: R$ {format(base_ir, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 10833/03 - CSLL: 0,01: R$ {format(base_cssl, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 116/03 - ISS: {format(base_iss, '.4f').replace('.', ',')}|\n\n TOTAL LIQUIDO A RECEBER: R$ {format(total_liquido_descricao, '.4f').replace('.', ',')}|"


        #################################### COM ANS ######################################################



        if nota.tipo_de_faturamento == 'FATURAMENTO HORAS' and nota.cnpj_da_nota.tipo_de_cliente == 'LOG' and nota.porcentagem_ans is not None:
            descricao = f"PRESTAÇÃO DE SERVIÇOS DE APOIO A OPERAÇÃO DE ARMAZENAGEM E LOGISTICA|\n\nCONTRATO: {nota.baseinfocontratos.contrato} - COMPETÊNCIA: {nota.competencia_nota}|\n\n TODOS OS ITENS DESCRITOS NA NF SOFRERAM DESCONTO DE {nota.porcentagem_ans} % PELA PONTUAÇÃO DO ANS NA COMPETÊNCIA DE {nota.competencia_nota_ans.competencia}.|"
            for baseinfocontratos_field, quantidade_hora_field in [('baseinfocontratos', 'quantidade_hora'), ('baseinfocontratos2', 'quantidade_hora2'), ('baseinfocontratos3', 'quantidade_hora3'), ('baseinfocontratos4', 'quantidade_hora4'), ('baseinfocontratos5', 'quantidade_hora5'), ('baseinfocontratos6', 'quantidade_hora6'), ('baseinfocontratos7', 'quantidade_hora7'), ('baseinfocontratos8', 'quantidade_hora8')]:  # adicione aqui todos os pares baseinfocontratos/quantidade_hora
                baseinfocontratos = getattr(nota, baseinfocontratos_field)
                quantidade_hora = getattr(nota, quantidade_hora_field)
                if baseinfocontratos and quantidade_hora:
                    total_bruto_cargo = round(baseinfocontratos.valor_hora * Decimal(str(quantidade_hora)), 4)
                    total_bruto_cargo_ans = round(total_bruto_cargo - (total_bruto_cargo * Decimal(str(nota.porcentagem_ans))), 4)
                    total_bruto_cargo_ans = str(total_bruto_cargo_ans).replace('.', ',')  # substitui o ponto por vírgula
                    descricao += f"CARGO: {baseinfocontratos.cargo} - QTD HS: {quantidade_hora}- VALOR HORA: R${baseinfocontratos.valor_hora} TOTAL BRUTO CARGO COM DESCONTO: R$ {total_bruto_cargo_ans}|\n\n"
            descricao += f"||TOTAL A FATURAR: R$ {format(total_a_faturar_nota, '.4f').replace('.', ',')}|\n\n BASE PARA RETENÇÕES:|\n\nRETENÇÃO CONFORME LEI 10833/03 - PIS: 0,0065: R$ {format(base_pis, '.4f').replace('.', ',')}|\n\nRETENÇÃO CONFORME LEI 10833/03 - CONFINS: 0,03: R$ {format(base_confins, '.4f').replace('.', ',')}|\n\n INSS RETENÇÃO: 0,11: R$ {format(base_inss, '.4f').replace('.', ',')}|\n\n I.R. RETENÇÃO: 0,048: R$ {format(base_ir, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 10833/03 - CSLL: 0,01: R$ {format(base_cssl, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 116/03 - ISS: {format(base_iss, '.4f').replace('.', ',')}|\n\n TOTAL LIQUIDO A RECEBER: R$ {format(total_liquido_descricao, '.4f').replace('.', ',')}|"


        #################################### REPACTUAÇÃO######################################################



        if nota.tipo_de_faturamento == 'FATURAMENTO REPACTUAÇÃO E REQUILIBRIO' and nota.porcentagem_ans is None:
            descricao = f"CONTRATO: {nota.contrato_texto_livre} |\n\n | {nota.texto_livre}"
            
            descricao += f"||TOTAL A FATURAR: R$ {format(total_a_faturar_nota, '.4f').replace('.', ',')}|\n\n BASE PARA RETENÇÕES:|\n\nRETENÇÃO CONFORME LEI 10833/03 - PIS: 0,0065: R$ {format(base_pis, '.4f').replace('.', ',')}|\n\nRETENÇÃO CONFORME LEI 10833/03 - CONFINS: 0,03: R$ {format(base_confins, '.4f').replace('.', ',')}|\n\n INSS RETENÇÃO: 0,11: R$ {format(base_inss, '.4f').replace('.', ',')}|\n\n I.R. RETENÇÃO: 0,048: R$ {format(base_ir, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 10833/03 - CSLL: 0,01: R$ {format(base_cssl, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 116/03 - ISS: {format(base_iss, '.4f').replace('.', ',')}|\n\n TOTAL LIQUIDO A RECEBER: R$ {format(total_liquido_descricao, '.4f').replace('.', ',')}|"


        #################################### PRIVADOS######################################################



        if nota.tipo_de_faturamento == 'FATURAMENTO OUTROS' and nota.porcentagem_ans is None:
            descricao = f"{nota.texto_livre}"
            
            descricao += f"||TOTAL A FATURAR: R$ {format(total_a_faturar_nota, '.4f').replace('.', ',')}|\n\n BASE PARA RETENÇÕES:|\n\nRETENÇÃO CONFORME LEI 10833/03 - PIS: 0,0065: R$ {format(base_pis, '.4f').replace('.', ',')}|\n\nRETENÇÃO CONFORME LEI 10833/03 - CONFINS: 0,03: R$ {format(base_confins, '.4f').replace('.', ',')}|\n\n INSS RETENÇÃO: 0,11: R$ {format(base_inss, '.4f').replace('.', ',')}|\n\n I.R. RETENÇÃO: 0,048: R$ {format(base_ir, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 10833/03 - CSLL: 0,01: R$ {format(base_cssl, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 116/03 - ISS: {format(base_iss, '.4f').replace('.', ',')}|\n\n TOTAL LIQUIDO A RECEBER: R$ {format(total_liquido_descricao, '.4f').replace('.', ',')}|"





        # aqui, você pode adicionar os outros casos 'MOT' e 'DISTRIBUIÇÃO' de maneira similar
        return descricao

    field_mappings = {
        'D': lambda nota: 'D',
        'sequencial': lambda nota: nota.id,
        'id': lambda nota: nota.id,
        'data_emissao': lambda nota: today,
        'N': lambda nota: 'N',
        'field_total': lambda nota: nota.total_quantidade_de_horas,
        'cnpj_tipo_de_servico': lambda nota: getattr(nota.cnpj_da_nota, 'tipo_de_servico', ''),
        'S': lambda nota: 'S',
        'sempre_em_branco': lambda nota: '',
        'cnpj_cnpj': lambda nota: re.sub(r'\D', '', getattr(nota.cnpj_da_nota, 'cnpj', '')),
        'cnpj_razao': lambda nota: getattr(nota.cnpj_da_nota, 'razao', ''),
        'cnpj_avenida_rua': lambda nota: getattr(nota.cnpj_da_nota, 'avenida_rua', ''),
        'cnpj_endereco': lambda nota: getattr(nota.cnpj_da_nota, 'endereco', ''),
        'cnpj_numero': lambda nota: getattr(nota.cnpj_da_nota, 'numero', ''),
        'cnpj_complemento': lambda nota: getattr(nota.cnpj_da_nota, 'complemento', ''),
        'cnpj_bairro': lambda nota: getattr(nota.cnpj_da_nota, 'bairro', ''),
        'cnpj_municipio': lambda nota: getattr(nota.cnpj_da_nota, 'municipio', ''),
        'cnpj_uf': lambda nota: getattr(nota.cnpj_da_nota, 'uf', ''),
        'cnpj_cep': lambda nota: getattr(nota.cnpj_da_nota, 'cep', ''),
        'email': lambda nota: 'alex.sobreira@go2b.com.br',    
        'id_2': lambda nota: nota.id,
        'descricao': generate_description,
        '0': lambda nota: '0',
    }
    sequential_number = 1  # iniciando o número sequencial para a segunda coluna

    for nota in notas:
        row = []
        for field, get_value in field_mappings.items():
            if field == 'sequencial':
                valor = sequential_number
                sequential_number += 1
            else:
                valor = get_value(nota)
            row.append(valor)
        writer.writerow(row)

    return response






def generate_csv_for_nota(request, pk):
    nota = Notas.objects.get(pk=pk)
    notas = [nota]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="notas.csv"'

    writer = csv.writer(response, delimiter=';')
    today = timezone.now().strftime("%Y-%m-%d")
    test_marker = 'T' if 'test' in request.GET else ''
    first_row = ['H', today, today, test_marker, '18504752000155']
    writer.writerow(first_row)

    def generate_description(nota):
        descricao = ""
        if nota.porcentagem_ans is not None and nota.total_valor_outros is None:
            total_a_faturar_nota = round(nota.total_a_faturar - (nota.total_a_faturar * nota.porcentagem_ans) , 4)

        elif nota.porcentagem_ans is None and nota.total_valor_outros is not None:
            total_a_faturar_nota = round(nota.total_valor_outros, 4)

        else:
            total_a_faturar_nota = round(nota.total_a_faturar, 4) 

        base_pis = total_a_faturar_nota * Decimal("0.0065")
        base_confins = total_a_faturar_nota * Decimal("0.03")
        base_inss = total_a_faturar_nota * Decimal("0.11")
        base_ir = total_a_faturar_nota * Decimal("0.048")
        base_cssl = total_a_faturar_nota * Decimal("0.01")
        base_iss = total_a_faturar_nota * nota.cnpj_da_nota.iss
        total_liquido_descricao = round(total_a_faturar_nota - (base_pis + base_confins + base_inss + base_ir + base_cssl + base_iss) , 4)



        if nota.tipo_de_faturamento == 'FATURAMENTO HORAS' and nota.cnpj_da_nota.tipo_de_cliente == 'LOG' and nota.porcentagem_ans is None:
            descricao = f"PRESTAÇÃO DE SERVIÇOS DE APOIO A OPERAÇÃO DE ARMAZENAGEM E LOGISTICA|\n\nCONTRATO: {nota.baseinfocontratos.contrato} - COMPETÊNCIA: {nota.competencia_nota}|\n\n"
            for baseinfocontratos_field, quantidade_hora_field in [('baseinfocontratos', 'quantidade_hora'), ('baseinfocontratos2', 'quantidade_hora2'), ('baseinfocontratos3', 'quantidade_hora3'), ('baseinfocontratos4', 'quantidade_hora4'), ('baseinfocontratos5', 'quantidade_hora5'), ('baseinfocontratos6', 'quantidade_hora6'), ('baseinfocontratos7', 'quantidade_hora7'), ('baseinfocontratos8', 'quantidade_hora8')]:  # adicione aqui todos os pares baseinfocontratos/quantidade_hora
                baseinfocontratos = getattr(nota, baseinfocontratos_field)
                quantidade_hora = getattr(nota, quantidade_hora_field)
                if baseinfocontratos and quantidade_hora:
                    total_bruto_cargo = round(baseinfocontratos.valor_hora * Decimal(str(quantidade_hora)), 4)
                    total_bruto_cargo = str(total_bruto_cargo).replace('.', ',')  # substitui o ponto por vírgula
                    descricao += f"CARGO: {baseinfocontratos.cargo} - QTD HS: {quantidade_hora}- VALOR HORA: R${baseinfocontratos.valor_hora} TOTAL BRUTO CARGO: R$ {total_bruto_cargo}|\n\n"
            descricao += f"||TOTAL A FATURAR: R$ {format(total_a_faturar_nota, '.4f').replace('.', ',')}|\n\n BASE PARA RETENÇÕES:|\n\nRETENÇÃO CONFORME LEI 10833/03 - PIS: 0,0065: R$ {format(base_pis, '.4f').replace('.', ',')}|\n\nRETENÇÃO CONFORME LEI 10833/03 - CONFINS: 0,03: R$ {format(base_confins, '.4f').replace('.', ',')}|\n\n INSS RETENÇÃO: 0,11: R$ {format(base_inss, '.4f').replace('.', ',')}|\n\n I.R. RETENÇÃO: 0,048: R$ {format(base_ir, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 10833/03 - CSLL: 0,01: R$ {format(base_cssl, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 116/03 - ISS: {format(base_iss, '.4f').replace('.', ',')}|\n\n TOTAL LIQUIDO A RECEBER: R$ {format(total_liquido_descricao, '.4f').replace('.', ',')}|"


        if nota.tipo_de_faturamento == 'FATURAMENTO HORAS' and nota.cnpj_da_nota.tipo_de_cliente == 'MOT' and nota.porcentagem_ans is None:
            descricao = f"PRESTAÇÃO DE SERVIÇOS DE APOIO A OPERAÇÃO DE ARMAZENAGEM E LOGISTICA|\n\nCONTRATO: {nota.baseinfocontratos.contrato} - COMPETÊNCIA: {nota.competencia_nota}|\n\n"
            for baseinfocontratos_field, quantidade_hora_field in [('baseinfocontratos', 'quantidade_hora'), ('baseinfocontratos2', 'quantidade_hora2'), ('baseinfocontratos3', 'quantidade_hora3'), ('baseinfocontratos4', 'quantidade_hora4'), ('baseinfocontratos5', 'quantidade_hora5'), ('baseinfocontratos6', 'quantidade_hora6'), ('baseinfocontratos7', 'quantidade_hora7'), ('baseinfocontratos8', 'quantidade_hora8')]:  # adicione aqui todos os pares baseinfocontratos/quantidade_hora
                baseinfocontratos = getattr(nota, baseinfocontratos_field)
                quantidade_hora = getattr(nota, quantidade_hora_field)
                if baseinfocontratos and quantidade_hora:
                    total_bruto_cargo = round(baseinfocontratos.valor_hora * Decimal(str(quantidade_hora)), 4)
                    total_bruto_cargo = str(total_bruto_cargo).replace('.', ',')  # substitui o ponto por vírgula
                    descricao += f"CARGO: {baseinfocontratos.cargo} - QTD HS: {quantidade_hora}- VALOR HORA: R${baseinfocontratos.valor_hora} TOTAL BRUTO CARGO: R$ {total_bruto_cargo}|\n\n"
            descricao += f"||TOTAL A FATURAR: R$ {format(total_a_faturar_nota, '.4f').replace('.', ',')}|\n\n BASE PARA RETENÇÕES:|\n\nRETENÇÃO CONFORME LEI 10833/03 - PIS: 0,0065: R$ {format(base_pis, '.4f').replace('.', ',')}|\n\nRETENÇÃO CONFORME LEI 10833/03 - CONFINS: 0,03: R$ {format(base_confins, '.4f').replace('.', ',')}|\n\n INSS RETENÇÃO: 0,11: R$ {format(base_inss, '.4f').replace('.', ',')}|\n\n I.R. RETENÇÃO: 0,048: R$ {format(base_ir, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 10833/03 - CSLL: 0,01: R$ {format(base_cssl, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 116/03 - ISS: {format(base_iss, '.4f').replace('.', ',')}|\n\n TOTAL LIQUIDO A RECEBER: R$ {format(total_liquido_descricao, '.4f').replace('.', ',')}|"


        if nota.tipo_de_faturamento == 'FATURAMENTO HORAS' and nota.cnpj_da_nota.tipo_de_cliente == 'DISTRIBUIÇÃO' and nota.porcentagem_ans is None:
            descricao = f"PRESTAÇÃO DE SERVIÇOS CONTINUADOS DE APOIO AS UNIDADE DE DISTRUIBUIÇÃO, UNIDADE: {nota.cnpj_da_nota.unidade} MCU: {nota.cnpj_da_nota.mcu}|\n\nCONTRATO: {nota.baseinfocontratos.contrato} - COMPETÊNCIA: {nota.competencia_nota}|\n\n"
            for baseinfocontratos_field, quantidade_hora_field in [('baseinfocontratos', 'quantidade_hora'), ('baseinfocontratos2', 'quantidade_hora2'), ('baseinfocontratos3', 'quantidade_hora3'), ('baseinfocontratos4', 'quantidade_hora4'), ('baseinfocontratos5', 'quantidade_hora5'), ('baseinfocontratos6', 'quantidade_hora6'), ('baseinfocontratos7', 'quantidade_hora7'), ('baseinfocontratos8', 'quantidade_hora8')]:  # adicione aqui todos os pares baseinfocontratos/quantidade_hora
                baseinfocontratos = getattr(nota, baseinfocontratos_field)
                quantidade_hora = getattr(nota, quantidade_hora_field)
                if baseinfocontratos and quantidade_hora:
                    total_bruto_cargo = round(baseinfocontratos.valor_hora * Decimal(str(quantidade_hora)), 4)
                    total_bruto_cargo = str(total_bruto_cargo).replace('.', ',')  # substitui o ponto por vírgula
                    descricao += f"CARGO: {baseinfocontratos.cargo} - QTD HS: {quantidade_hora}- VALOR HORA: R${baseinfocontratos.valor_hora} TOTAL BRUTO CARGO: R$ {total_bruto_cargo}|\n\n"
            descricao += f"||TOTAL A FATURAR: R$ {format(total_a_faturar_nota, '.4f').replace('.', ',')}|\n\n BASE PARA RETENÇÕES:|\n\nRETENÇÃO CONFORME LEI 10833/03 - PIS: 0,0065: R$ {format(base_pis, '.4f').replace('.', ',')}|\n\nRETENÇÃO CONFORME LEI 10833/03 - CONFINS: 0,03: R$ {format(base_confins, '.4f').replace('.', ',')}|\n\n INSS RETENÇÃO: 0,11: R$ {format(base_inss, '.4f').replace('.', ',')}|\n\n I.R. RETENÇÃO: 0,048: R$ {format(base_ir, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 10833/03 - CSLL: 0,01: R$ {format(base_cssl, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 116/03 - ISS: {format(base_iss, '.4f').replace('.', ',')}|\n\n TOTAL LIQUIDO A RECEBER: R$ {format(total_liquido_descricao, '.4f').replace('.', ',')}|"


        #################################### COM ANS ######################################################



        if nota.tipo_de_faturamento == 'FATURAMENTO HORAS' and nota.cnpj_da_nota.tipo_de_cliente == 'LOG' and nota.porcentagem_ans is not None:
            descricao = f"PRESTAÇÃO DE SERVIÇOS DE APOIO A OPERAÇÃO DE ARMAZENAGEM E LOGISTICA|\n\nCONTRATO: {nota.baseinfocontratos.contrato} - COMPETÊNCIA: {nota.competencia_nota}|\n\n TODOS OS ITENS DESCRITOS NA NF SOFRERAM DESCONTO DE {nota.porcentagem_ans} % PELA PONTUAÇÃO DO ANS NA COMPETÊNCIA DE {nota.competencia_nota_ans.competencia}.|"
            for baseinfocontratos_field, quantidade_hora_field in [('baseinfocontratos', 'quantidade_hora'), ('baseinfocontratos2', 'quantidade_hora2'), ('baseinfocontratos3', 'quantidade_hora3'), ('baseinfocontratos4', 'quantidade_hora4'), ('baseinfocontratos5', 'quantidade_hora5'), ('baseinfocontratos6', 'quantidade_hora6'), ('baseinfocontratos7', 'quantidade_hora7'), ('baseinfocontratos8', 'quantidade_hora8')]:  # adicione aqui todos os pares baseinfocontratos/quantidade_hora
                baseinfocontratos = getattr(nota, baseinfocontratos_field)
                quantidade_hora = getattr(nota, quantidade_hora_field)
                if baseinfocontratos and quantidade_hora:
                    total_bruto_cargo = round(baseinfocontratos.valor_hora * Decimal(str(quantidade_hora)), 4)
                    total_bruto_cargo_ans = round(total_bruto_cargo - (total_bruto_cargo * Decimal(str(nota.porcentagem_ans))), 4)
                    total_bruto_cargo_ans = str(total_bruto_cargo_ans).replace('.', ',')  # substitui o ponto por vírgula
                    descricao += f"CARGO: {baseinfocontratos.cargo} - QTD HS: {quantidade_hora}- VALOR HORA: R${baseinfocontratos.valor_hora} TOTAL BRUTO CARGO COM DESCONTO: R$ {total_bruto_cargo_ans}|\n\n"
            descricao += f"||TOTAL A FATURAR: R$ {format(total_a_faturar_nota, '.4f').replace('.', ',')}|\n\n BASE PARA RETENÇÕES:|\n\nRETENÇÃO CONFORME LEI 10833/03 - PIS: 0,0065: R$ {format(base_pis, '.4f').replace('.', ',')}|\n\nRETENÇÃO CONFORME LEI 10833/03 - CONFINS: 0,03: R$ {format(base_confins, '.4f').replace('.', ',')}|\n\n INSS RETENÇÃO: 0,11: R$ {format(base_inss, '.4f').replace('.', ',')}|\n\n I.R. RETENÇÃO: 0,048: R$ {format(base_ir, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 10833/03 - CSLL: 0,01: R$ {format(base_cssl, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 116/03 - ISS: {format(base_iss, '.4f').replace('.', ',')}|\n\n TOTAL LIQUIDO A RECEBER: R$ {format(total_liquido_descricao, '.4f').replace('.', ',')}|"


        #################################### REPACTUAÇÃO######################################################



        if nota.tipo_de_faturamento == 'FATURAMENTO REPACTUAÇÃO E REQUILIBRIO' and nota.porcentagem_ans is None:
            descricao = f"CONTRATO: {nota.contrato_texto_livre} |\n\n | {nota.texto_livre}"
            
            descricao += f"||TOTAL A FATURAR: R$ {format(total_a_faturar_nota, '.4f').replace('.', ',')}|\n\n BASE PARA RETENÇÕES:|\n\nRETENÇÃO CONFORME LEI 10833/03 - PIS: 0,0065: R$ {format(base_pis, '.4f').replace('.', ',')}|\n\nRETENÇÃO CONFORME LEI 10833/03 - CONFINS: 0,03: R$ {format(base_confins, '.4f').replace('.', ',')}|\n\n INSS RETENÇÃO: 0,11: R$ {format(base_inss, '.4f').replace('.', ',')}|\n\n I.R. RETENÇÃO: 0,048: R$ {format(base_ir, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 10833/03 - CSLL: 0,01: R$ {format(base_cssl, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 116/03 - ISS: {format(base_iss, '.4f').replace('.', ',')}|\n\n TOTAL LIQUIDO A RECEBER: R$ {format(total_liquido_descricao, '.4f').replace('.', ',')}|"


        #################################### PRIVADOS######################################################



        if nota.tipo_de_faturamento == 'FATURAMENTO OUTROS' and nota.porcentagem_ans is None:
            descricao = f"{nota.texto_livre}"
            
            descricao += f"||TOTAL A FATURAR: R$ {format(total_a_faturar_nota, '.4f').replace('.', ',')}|\n\n BASE PARA RETENÇÕES:|\n\nRETENÇÃO CONFORME LEI 10833/03 - PIS: 0,0065: R$ {format(base_pis, '.4f').replace('.', ',')}|\n\nRETENÇÃO CONFORME LEI 10833/03 - CONFINS: 0,03: R$ {format(base_confins, '.4f').replace('.', ',')}|\n\n INSS RETENÇÃO: 0,11: R$ {format(base_inss, '.4f').replace('.', ',')}|\n\n I.R. RETENÇÃO: 0,048: R$ {format(base_ir, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 10833/03 - CSLL: 0,01: R$ {format(base_cssl, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 116/03 - ISS: {format(base_iss, '.4f').replace('.', ',')}|\n\n TOTAL LIQUIDO A RECEBER: R$ {format(total_liquido_descricao, '.4f').replace('.', ',')}|"





        # aqui, você pode adicionar os outros casos 'MOT' e 'DISTRIBUIÇÃO' de maneira similar
        return descricao

    field_mappings = {
        'D': lambda nota: 'D',
        'sequencial': lambda nota: nota.id,
        'id': lambda nota: nota.id,
        'data_emissao': lambda nota: today,
        'N': lambda nota: 'N',
        'field_total': lambda nota: nota.total_quantidade_de_horas,
        'cnpj_tipo_de_servico': lambda nota: getattr(nota.cnpj_da_nota, 'tipo_de_servico', ''),
        'S': lambda nota: 'S',
        'sempre_em_branco': lambda nota: '',
        'cnpj_cnpj': lambda nota: re.sub(r'\D', '', getattr(nota.cnpj_da_nota, 'cnpj', '')),
        'cnpj_razao': lambda nota: getattr(nota.cnpj_da_nota, 'razao', ''),
        'cnpj_avenida_rua': lambda nota: getattr(nota.cnpj_da_nota, 'avenida_rua', ''),
        'cnpj_endereco': lambda nota: getattr(nota.cnpj_da_nota, 'endereco', ''),
        'cnpj_numero': lambda nota: getattr(nota.cnpj_da_nota, 'numero', ''),
        'cnpj_complemento': lambda nota: getattr(nota.cnpj_da_nota, 'complemento', ''),
        'cnpj_bairro': lambda nota: getattr(nota.cnpj_da_nota, 'bairro', ''),
        'cnpj_municipio': lambda nota: getattr(nota.cnpj_da_nota, 'municipio', ''),
        'cnpj_uf': lambda nota: getattr(nota.cnpj_da_nota, 'uf', ''),
        'cnpj_cep': lambda nota: getattr(nota.cnpj_da_nota, 'cep', ''),
        'email': lambda nota: 'alex.sobreira@go2b.com.br',    
        'id_2': lambda nota: nota.id,
        'descricao': generate_description,
        '0': lambda nota: '0',
    }
    sequential_number = 1  # iniciando o número sequencial para a segunda coluna

    for nota in notas:
        row = []
        for field, get_value in field_mappings.items():
            if field == 'sequencial':
                valor = sequential_number
                sequential_number += 1
            else:
                valor = get_value(nota)
            row.append(valor)
        writer.writerow(row)

    return response
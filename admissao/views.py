import os
from subprocess import Popen

from django.conf import settings
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from docx import Document
from docx2pdf import convert
from docx2pdf import convert as convert_docx_to_pdf
from rest_framework import generics
from zeep import Client

from .forms import Admissao, AdmissaoForm, UploadFileForm
from .models import Base, Collaborator, ContractTemplate, Departamento, Turno
from .serializers import (BaseSerializer, DepartamentoSerializer,
                          TurnoSerializer)

########################################################################













########################################################################

##########################BUSCA COLABORADOR#############################




class CollaboratorSearchView(ListView):
    model = Collaborator
    template_name = 'admissao/busca_de_candidatos.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['order_by'] = self.request.GET.get('order_by', '-id')
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
        order_by = self.request.GET.get('order_by', '-id')
        if query:
            return Collaborator.objects.filter(Q(cpf__icontains=query)).order_by(order_by)
        return Collaborator.objects.all().order_by(order_by)





#############################ATUALIZAÇÃO################################


class CollaboratorUpdateView(UpdateView):
    model = Collaborator
    template_name = 'admissao/formulario_adm_rh.html'
    fields = '__all__'
    success_url = reverse_lazy('search_collaborator')


############################DETALHAMENTO################################

class CollaboratorDetailView(DetailView):
    model = Collaborator
    template_name = 'admissao/collaborator_detail.html'
    

#######################ADMISSÃO COLABORADOR#############################

class AdmissaoCreateView(CreateView):
    model = Collaborator
    form_class = Admissao
    template_name = 'admissao/formulario_adm.html'  # substitua com o seu template
    success_url = reverse_lazy('admissao')  # substitua com a URL que você quer redirecionar após o sucesso

    def form_valid(self, form):
        cpf = form.cleaned_data.get('cpf')
        collaborator = Collaborator.objects.filter(cpf=cpf).first()
        
        if collaborator:
            # Atualizar o objeto existente
            for field, value in form.cleaned_data.items():
                if value is not None and hasattr(collaborator, field) and field != 'created_by':
                    setattr(collaborator, field, value)
            collaborator.save()
            self.object = collaborator
        else:
            # Criar um novo objeto
            if self.request.user.is_authenticated:
                form.instance.created_by = self.request.user
            self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def validate_cpf(value):
        if len(value) != 11 or not value.isdigit():
            return False
        cpf = [int(char) for char in value]
        if cpf == cpf[::-1]:
            return False
        for i in range(9):
            val = sum((cpf[num] * ((10-i) % 11)) for num in range(0, 10))
            digit = ((val * 10) % 11) % 10
            if digit != cpf[9]:
                return False
        val = sum((cpf[num] * ((11-i) % 11)) for num in range(0, 11))
        digit = ((val * 10) % 11) % 10
        if digit != cpf[10]:
            return False
        return True


class AdmissaoRHCreateView(CreateView):
    model = Collaborator
    form_class = AdmissaoForm
    template_name = 'admissao/formulario_adm_rh.html'
    success_url = reverse_lazy('admissao_rh')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Erro no campo '{form.fields[field].label}': {error}")
        return super().form_invalid(form)
    
########################################################################

    











########################################################################

##########################SUBIR TEMPLATE################################
def upload_template(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_template = ContractTemplate(name=form.cleaned_data['name'], file=request.FILES['file'])
            new_template.save()
            return HttpResponseRedirect('/upload_template')  # Redirect to a page showing success.
    else:
        form = UploadFileForm()
    return render(request, 'admissao/upload.html', {'form': form})

########################################################################

####################GERAÇÃO DO CONTRATO EM PDF##########################

def generate_contract(template, collaborator):
    # Load the Word document
    doc = Document(template.file.path)

    # Prepare the replacement dictionary combining values from all models
    replacements = {}
    replacements.update(collaborator.get_field_values())
    if collaborator.departamento:
        replacements.update(collaborator.departamento.get_field_values())
    if collaborator.cliente_gi:
        replacements.update(collaborator.cliente_gi.get_field_values())
    if collaborator.turno:
        replacements.update(collaborator.turno.get_field_values())
    if collaborator.cargo:
        replacements.update(collaborator.cargo.get_field_values())

    # Loop through each paragraph
    for paragraph in doc.paragraphs:
        # Replace the keys in the entire paragraph text, not just the runs
        inline = paragraph.runs
        for key, value in replacements.items():
            if key in paragraph.text:
                text = paragraph.text.replace(key, value)
                for i in range(len(inline)):
                    if key in inline[i].text:
                        text = inline[i].text.replace(key, value)
                        inline[i].text = text

    # Make sure the contracts directory exists
    contract_directory = os.path.join(settings.MEDIA_ROOT, 'contracts')
    os.makedirs(contract_directory, exist_ok=True)

    # Save the new Word document
    new_contract_filename = os.path.join(contract_directory, f'{collaborator.name}_{template.name}.docx')
    doc.save(new_contract_filename)

    # Convert the Word document to PDF
    new_contract_pdf_filename = os.path.join(contract_directory, f'{collaborator.name}_{template.name}.pdf')
    p = Popen(['libreoffice', '--headless', '--convert-to', 'pdf', new_contract_filename, '--outdir', contract_directory])
    #print("Waiting for conversion...")
    p.wait()
    #print("Conversion finished.")

    # Delete the Word document
    os.remove(new_contract_filename)

    return new_contract_pdf_filename

def convert_to_pdf(input_filepath, output_filepath):
    convert(input_filepath, output_filepath)

def select_contract(request):
    if request.method == 'POST':
        collaborator_id = request.POST.get('collaborator')
        template_id = request.POST.get('template')

        collaborator = Collaborator.objects.get(id=collaborator_id)
        template = ContractTemplate.objects.get(id=template_id)

        contract_filename = generate_contract(template, collaborator)

        return FileResponse(open(contract_filename, 'rb'), as_attachment=True, filename=os.path.basename(contract_filename), content_type='application/pdf')

    collaborators = Collaborator.objects.all()
    templates = ContractTemplate.objects.all()

    return render(request, 'admissao/select_contract.html', {'collaborators': collaborators, 'templates': templates})


def select_contract_id(request, collaborator_id):
    if request.method == 'POST':
        template_id = request.POST.get('template')

        collaborator = Collaborator.objects.get(id=collaborator_id)
        template = ContractTemplate.objects.get(id=template_id)

        contract_filename = generate_contract(template, collaborator)
        
        # Vamos obter apenas o nome do arquivo sem o caminho
        filename = os.path.basename(contract_filename)

        # Retornamos o arquivo como anexo, definindo o nome do arquivo no cabeçalho 'Content-Disposition'
        return FileResponse(open(contract_filename, 'rb'), as_attachment=True, filename=filename, content_type='application/pdf')

    # Agora, se o request não for POST, o colaborador será buscado pelo parâmetro na URL:
    else:
        collaborator = Collaborator.objects.get(id=collaborator_id)
        templates = ContractTemplate.objects.all()

        return render(request, 'admissao/select_contract_id.html', {'collaborator': collaborator, 'templates': templates})





########################################################################


###################CONFIGURAÇÕES PARA O FILTRO NO FORM##################


class DepartamentoList(generics.ListAPIView):
    serializer_class = DepartamentoSerializer

    def get_queryset(self):
        cliente_gi_id = self.request.query_params.get('cliente_gi_id', None)
        if cliente_gi_id is not None:
            return Departamento.objects.filter(cliente_gi_dep=cliente_gi_id)
        return Departamento.objects.none()

class BaseList(generics.ListAPIView):
    serializer_class = BaseSerializer

    def get_queryset(self):
        cliente_gi_id = self.request.query_params.get('cliente_gi_id', None)
        if cliente_gi_id is not None:
            return Base.objects.filter(cliente=cliente_gi_id)
        return Base.objects.none()
    
class TurnoList(generics.ListAPIView):
    serializer_class = TurnoSerializer

    def get_queryset(self):
        departamento_id = self.request.query_params.get('departamento_id', None)
        if departamento_id is not None:
            return Turno.objects.filter(departamento=departamento_id)
        return Turno.objects.none()



############################################################################
import os

from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import FileResponse, HttpResponseRedirect, JsonResponse
# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from docx import Document
from docx2pdf import convert
from rest_framework import generics

from .forms import Admissao, AdmissaoForm, UploadFileForm
from .models import Base, Collaborator, ContractTemplate, Departamento, Turno
from .serializers import (BaseSerializer, DepartamentoSerializer,
                          TurnoSerializer)


class CollaboratorUpdateView(UpdateView):
    model = Collaborator
    template_name = 'collaborator_form.html'
    fields = '__all__'
    success_url = reverse_lazy('search_collaborator')

class CollaboratorDetailView(DetailView):
    model = Collaborator
    template_name = 'collaborator_detail.html'  # substitua com o seu template


class CollaboratorSearchView(ListView):
    model = Collaborator
    template_name = 'search_collaborator.html'  # substitua com o seu template

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Collaborator.objects.filter(Q(cpf__icontains=query))
        return Collaborator.objects.all()


class AdmissaoCreateView(CreateView):
    model = Collaborator
    form_class = Admissao
    template_name = 'formulario_adm.html'  # substitua com o seu template
    success_url = reverse_lazy('admissao')  # substitua com a URL que você quer redirecionar após o sucesso

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class AdmissaoRHCreateView(CreateView):
    model = Collaborator
    form_class = AdmissaoForm
    template_name = 'formulario_adm_rh.html'
    success_url = reverse_lazy('admissao_rh')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Erro no campo '{form.fields[field].label}': {error}")
        return super().form_invalid(form)
    

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
    




def convert_to_pdf(input_filepath, output_filepath):
    convert(input_filepath, output_filepath)



def upload_template(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_template = ContractTemplate(name=form.cleaned_data['name'], file=request.FILES['file'])
            new_template.save()
            return HttpResponseRedirect('/upload_template')  # Redirect to a page showing success.
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})



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

    return new_contract_filename

def select_contract(request):
    if request.method == 'POST':
        collaborator_id = request.POST.get('collaborator')
        template_id = request.POST.get('template')

        collaborator = Collaborator.objects.get(id=collaborator_id)
        template = ContractTemplate.objects.get(id=template_id)

        contract_filename = generate_contract(template, collaborator)

        return FileResponse(open(contract_filename, 'rb'), as_attachment=True, filename=contract_filename)

    collaborators = Collaborator.objects.all()
    templates = ContractTemplate.objects.all()

    return render(request, 'select_contract.html', {'collaborators': collaborators, 'templates': templates})

def select_contract_id(request, collaborator_id):
    if request.method == 'POST':
        template_id = request.POST.get('template')

        collaborator = Collaborator.objects.get(id=collaborator_id)
        template = ContractTemplate.objects.get(id=template_id)

        contract_filename = generate_contract(template, collaborator)

        return FileResponse(open(contract_filename, 'rb'), as_attachment=True, filename=contract_filename)

    # Agora, se o request não for POST, o colaborador será buscado pelo parâmetro na URL:
    else:
        collaborator = Collaborator.objects.get(id=collaborator_id)
        templates = ContractTemplate.objects.all()

        return render(request, 'select_contract_id.html', {'collaborator': collaborator, 'templates': templates})


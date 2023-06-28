from django import forms
from django.core.exceptions import ValidationError
from validate_docbr import CPF

from .models import (Base, ClienteGI, Collaborator, ContractTemplate,
                     Departamento)


class TemplateSelectForm(forms.Form):
    template = forms.ModelChoiceField(queryset=ContractTemplate.objects.all())

class UploadFileForm(forms.Form):
    name = forms.CharField(max_length=200)
    file = forms.FileField()

class Admissao(forms.ModelForm):
    class Meta:
        model = Collaborator
        fields = ['name', 'cpf', 'rg', 'orgao_emissor_rg', 'uf_rg', 'data_emissao_rg', 'n_ctps', 'serie', 'uf_ctps', 'data_emissao_ctps', 'endereco', 'cep', 'celular', 'email']
        requireds = ['name', 'cpf', 'rg', 'orgao_emissor_rg', 'uf_rg', 'data_emissao_rg', 'n_ctps', 'serie', 'uf_ctps', 'data_emissao_ctps', 'endereco', 'cep', 'celular', 'email']

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        cpf_validator = CPF()

        if cpf and not cpf_validator.validate(cpf):
            raise ValidationError('CPF inválido')
        
        return cpf

class AdmissaoForm(forms.ModelForm):
    class Meta:
        model = Collaborator
        fields = '__all__'



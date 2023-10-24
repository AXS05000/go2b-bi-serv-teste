from django import forms

from .models import Funcionario


class SelecionarFuncionarioForm(forms.Form):

    class Meta:
        model = Funcionario
        fields = ['codigo_fc', 'comp']


    codigo_fc = forms.IntegerField()
    comp = forms.IntegerField()


class DeleteCompForm(forms.Form):
    comp = forms.IntegerField()


class AutenticacaoForm(forms.Form):
    autenticacao = forms.CharField(max_length=200)
    competencia = forms.CharField(max_length=200)


class UploadFileForm(forms.Form):
    file = forms.FileField()


class CompetenciaForm(forms.Form):
    competencia = forms.CharField(label='Competência', max_length=200)


class OtimizacaoForm(forms.Form):
    competencia = forms.CharField(label='Competência', max_length=200)


class UploadExcelForm(forms.Form):
    excel_file = forms.FileField(label='Selecione um arquivo Excel')

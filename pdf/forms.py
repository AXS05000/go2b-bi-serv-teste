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
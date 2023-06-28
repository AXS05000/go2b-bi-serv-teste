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

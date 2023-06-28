from django import forms
from django.core.exceptions import ValidationError
from django.core.mail.message import EmailMessage

from .models import BaseCNPJ, Notas


class NotasModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = Notas
        fields = ['baseinfocontratos', 'cnpj_da_nota', 'competencia_nota', 'tipo_de_faturamento', 'porcentagem_ans','competencia_nota_ans', 'quantidade_hora','baseinfocontratos2', 'quantidade_hora2','baseinfocontratos3', 'quantidade_hora3','baseinfocontratos4', 'quantidade_hora4','baseinfocontratos5', 'quantidade_hora5','baseinfocontratos6', 'quantidade_hora6','baseinfocontratos7', 'quantidade_hora7','baseinfocontratos8', 'quantidade_hora8','texto_livre','total_valor_outros', 'contrato_texto_livre']
        required = ['competencia_nota', 'tipo_de_faturamento', 'cnpj_da_nota']
        error_messages = {
            'porcentagem_ans': {
                'max_digits': 'Certifique-se de que tenha digitado o valor correto de porcentagem na ANS'
            },
            'quantidade_hora': {
                'max_digits': 'Valor digitado no 1° campo de horas passa de 100.000,00 horas verifique se digitou corretamente'
            },
            'quantidade_hora2': {
                'max_digits': 'Valor digitado no 2° campo de horas passa de 100.000,00 horas verifique se digitou corretamente'
            },
            'quantidade_hora3': {
                'max_digits': 'Valor digitado no 3° campo de horas passa de 100.000,00 horas verifique se digitou corretamente'
            },
            'quantidade_hora4': {
                'max_digits': 'Valor digitado no 4° campo de horas passa de 100.000,00 horas verifique se digitou corretamente'
            },
            'quantidade_hora5': {
                'max_digits': 'Valor digitado no 5° campo de horas passa de 100.000,00 horas verifique se digitou corretamente'
            },
            'quantidade_hora6': {
                'max_digits': 'Valor digitado no 6° campo de horas passa de 100.000,00 horas verifique se digitou corretamente'
            },
            'quantidade_hora7': {
                'max_digits': 'Valor digitado no 7° campo de horas passa de 100.000,00 horas verifique se digitou corretamente'
            },
            'quantidade_hora8': {
                'max_digits': 'Valor digitado no 8° campo de horas passa de 100.000,00 horas verifique se digitou corretamente'
            },

            
        }



class BaseCNPJModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = BaseCNPJ
        fields = ['cnpj', 'nome_cliente', 'unidade', 'razao','avenida_rua', 'endereco','numero', 'complemento','bairro', 'municipio','uf', 'cep', 'iss', 'tipo_de_servico']
        required = ['cnpj', 'nome_cliente', 'unidade', 'razao','avenida_rua', 'endereco','numero','bairro', 'municipio','uf', 'cep', 'iss', 'tipo_de_servico']

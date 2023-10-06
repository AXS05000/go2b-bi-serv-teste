from django import forms
from django.core.exceptions import ValidationError
from django.core.mail.message import EmailMessage

from .models import BaseCNPJ, BaseInfoContratos, Notas


class NotasModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.required:
            self.fields[field].required = True

        # Filtrar apenas contratos ativos
        self.fields['baseinfocontratos'].queryset = BaseInfoContratos.objects.filter(contrato_ativo=True)
        self.fields['porcentagem_ans'].widget.attrs.update({'placeholder': 'Exemplo: 0,05'})
                
        # O mesmo para os demais campos
        for i in range(2, 9):
            self.fields[f'baseinfocontratos{i}'].queryset = BaseInfoContratos.objects.filter(contrato_ativo=True)


    class Meta:
        model = Notas
        fields = ['baseinfocontratos', 'cnpj_da_nota', 'competencia_nota', 'texto_livre', 'tipo_de_faturamento', 'porcentagem_ans','competencia_nota_ans', 'quantidade_hora','baseinfocontratos2', 'quantidade_hora2','baseinfocontratos3', 'quantidade_hora3','baseinfocontratos4', 'quantidade_hora4','baseinfocontratos5', 'quantidade_hora5','baseinfocontratos6', 'quantidade_hora6','baseinfocontratos7', 'quantidade_hora7','baseinfocontratos8', 'quantidade_hora8','texto_livre','total_valor_outros', 'contrato_texto_livre']
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

        # Adicionando placeholders
        self.fields['cnpj'].widget.attrs.update({'placeholder': 'Exemplo: 34.208.316/2051-80'})
        self.fields['tipo_de_servico'].widget.attrs.update({'placeholder': 'Exemplo: 17.05'})
        self.fields['iss'].widget.attrs.update({'placeholder': 'Exemplo: 0,05'})   
        self.fields['cep'].widget.attrs.update({'placeholder': 'Exemplo: 88301970'})
        self.fields['razao'].widget.attrs.update({'placeholder': 'Exemplo: EMPRESA BRASILEIRA DE CORREIOS E TELEGRAFOS'})
        self.fields['avenida_rua'].widget.attrs.update({'placeholder': 'Exemplo: Em caso de Avenida (AV), Rua (RUA), Praça (PRACA)'})          
        self.fields['tx_adm'].widget.attrs.update({'placeholder': 'Exemplo: 0,035'})
        self.fields['mcu'].widget.attrs.update({'placeholder': 'Exemplo: 00056972'})
        self.fields['unidade'].widget.attrs.update({'placeholder': 'Exemplo: CEE ITAJAI'})
        self.fields['nome_cliente'].widget.attrs.update({'placeholder': 'Exemplo: ECT MOT - SC INTERIOR'})
        self.fields['endereco'].widget.attrs.update({'placeholder': 'Exemplo: CAMBORIU'})
        self.fields['numero'].widget.attrs.update({'placeholder': 'Exemplo: 640'})
        self.fields['complemento'].widget.attrs.update({'placeholder': 'Exemplo: CJ 2 ou pode deixar em branco caso não tenha.'})
        self.fields['bairro'].widget.attrs.update({'placeholder': 'Exemplo: FAZENDA'})
        self.fields['municipio'].widget.attrs.update({'placeholder': 'Exemplo: ITAJAI   '})
        self.fields['uf'].widget.attrs.update({'placeholder': 'Exemplo: SC'})
        
        

    class Meta:
        model = BaseCNPJ
        fields = ['cnpj', 'nome_cliente', 'unidade', 'razao','avenida_rua', 'endereco','numero', 'complemento','bairro', 'municipio','uf', 'cep', 'iss', 'tipo_de_servico', 'mcu', 'tx_adm', 'tipo_de_cliente']
        required = ['cnpj', 'nome_cliente', 'unidade', 'razao','avenida_rua', 'endereco','numero','bairro', 'municipio','uf', 'cep', 'iss', 'tipo_de_servico']




class BaseValorModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

        # Adicionando placeholders
        self.fields['cod_cliente'].widget.attrs.update({'placeholder': 'Exemplo: 5'})
        self.fields['contrato'].widget.attrs.update({'placeholder': 'Exemplo: 162-2021'})
        self.fields['cargo'].widget.attrs.update({'placeholder': 'Exemplo: AUX. OP DIU'})
        self.fields['valor_hora'].widget.attrs.update({'placeholder': 'Exemplo: 16,77'})
        self.fields['data_inicio_cto'].widget.attrs.update({'placeholder': 'Exemplo: 01/01/2023'})
        self.fields['contrato_ativo'].initial = True          
        
        

    class Meta:
        model = BaseInfoContratos
        fields = ['cod_cliente', 'contrato', 'cargo', 'valor_hora','data_inicio_cto', 'contrato_ativo']
        required = ['cod_cliente', 'contrato', 'cargo', 'valor_hora','data_inicio_cto']

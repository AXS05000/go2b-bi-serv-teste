from django.contrib import admin

from .models import (BaseCNPJ, BaseInfoContratos, Competencias, NotaFiscal2,
                     Notas)


@admin.register(BaseInfoContratos)
class BaseInfoContratosAdmin(admin.ModelAdmin):
    list_display = ('cod_cliente', 'contrato', 'cargo', 'valor_hora', 'data_inicio_cto', 'contrato_ativo')


@admin.register(Competencias)
class CompetenciasAdmin(admin.ModelAdmin):
    list_display = ('competencia',)

admin.site.register(NotaFiscal2)

@admin.register(Notas)
class NotasAdmin(admin.ModelAdmin):
    list_display = ('baseinfocontratos', 'porcentagem_ans','competencia_nota_ans', 'cnpj_da_nota', 'competencia_nota','tipo_de_faturamento', 'quantidade_hora','baseinfocontratos2', 'quantidade_hora2','baseinfocontratos3', 'quantidade_hora3','baseinfocontratos4', 'quantidade_hora4','baseinfocontratos5', 'quantidade_hora5','baseinfocontratos6', 'quantidade_hora6','baseinfocontratos7', 'quantidade_hora7','baseinfocontratos8', 'quantidade_hora8','texto_livre','total_valor_outros', 'contrato_texto_livre')

@admin.register(BaseCNPJ)
class BaseCNPJAdmin(admin.ModelAdmin):
    list_display = ('cnpj', 'nome_cliente', 'unidade','avenida_rua', 'endereco','numero', 'complemento','bairro', 'municipio','uf', 'cep', 'iss')

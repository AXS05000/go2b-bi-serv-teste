from django.urls import path

from . import views
from .views import (EditarNotaFiscalUpdateView, GerarcsvTemplateView,
                    NotaFiscalCreateView, Notas_FiscaisView)

urlpatterns = [
    path('notafiscal/', NotaFiscalCreateView.as_view(), name='notafiscal'),
    path('notasfiscais/', Notas_FiscaisView.as_view(), name='notasficais'),
    path('notasfiscais_editar/<int:pk>/', EditarNotaFiscalUpdateView.as_view(), name='editar_nota'),
    path('qtddecargos/', views.qtddecargos, name='qtddecargos'),
    path('notafiscal2/', views.notafiscal2, name='notafiscal2'),
    path('notafiscal3/', views.notafiscal3, name='notafiscal3'),
    path('notafiscal4/', views.notafiscal4, name='notafiscal4'),
    path('notafiscal5/', views.notafiscal5, name='notafiscal5'),
    path('notafiscal6/', views.notafiscal6, name='notafiscal6'),
    path('notafiscal7/', views.notafiscal7, name='notafiscal7'),
    path('notafiscal8/', views.notafiscal8, name='notafiscal8'),
    path('cnpj/', views.cnpj, name='cnpj'),
    path('form-valorhora/', views.form_valor_hora, name='form_valor_hora'),
    path('fatoutros/', views.fatoutros, name='fatoutros'),
    path('atualizar-cnpj/', views.update_basecnpj, name='atualizar_cnpj'),
    path('importar-cnpj/', views.import_basecnpj, name='importar_basecnpj'),
    path('importar-notas/', views.import_notas_, name='importar_notas_'),
    path('importar-baseinfo/', views.import_baseinfo, name='importar_baseinfo'),
    path('generate-csv/', views.generate_csv, name='generate-csv'),
    path('generate-txt/', views.generate_txt, name='generate-txt'),
    path('notas-s/', GerarcsvTemplateView.as_view(), name='gerar-csv'),
    path('buscar-notas/', views.buscar_notas, name='buscar_notas'),
    path('export/notas/', views.export_notas_excel, name='export_notas_excel'),
 
]
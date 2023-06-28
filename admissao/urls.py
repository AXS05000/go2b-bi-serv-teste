from django.urls import path

from . import views
from .views import (AdmissaoCreateView, AdmissaoRHCreateView, BaseList,
                    DepartamentoList, TurnoList)

urlpatterns = [
    path('gerar_contrato/', views.select_contract, name='select_contract'),
    path('gerar_contrato/<int:collaborator_id>/', views.select_contract_id, name='select_contract_id'),
    path('upload_template/', views.upload_template, name='upload_template'),
    path('admissao/', AdmissaoCreateView.as_view(), name='admissao'),
    path('admissao_rh/', AdmissaoRHCreateView.as_view(), name='admissao_rh'),
    path('api/departamentos/', DepartamentoList.as_view(), name='api-departamentos'),
    path('api/bases/', BaseList.as_view(), name='api-bases'),
    path('api/turnos/', TurnoList.as_view(), name='api-turnos'),
    path('candidatos/', views.CollaboratorSearchView.as_view(), name='search_collaborator'),
    path('colaborador/<int:pk>/', views.CollaboratorDetailView.as_view(), name='collaborator_detail'),
    path('editar/<int:pk>/', views.CollaboratorUpdateView.as_view(), name='edit_collaborator'),


]
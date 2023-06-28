from django.urls import path

from . import views

urlpatterns = [
    path('sf/', views.selecionar_funcionario, name='selecionar_funcionario'),
    path('sf2/', views.selecionar_funcionario2, name='selecionar_funcionario2'),
    path('gerar-pdf/<int:codigo_fc>/<int:comp>/', views.gerar_pdf_direto, name='gerar_pdf_direto'),
    path('gerar-pdf-2/<int:codigo_fc>/<int:comp>/', views.gerar_pdf_direto2, name='gerar_pdf_direto2'),
    path('upload/', views.upload_excel, name='upload_excel'),
    path('upload-bene/', views.upload_excel_bene, name='upload_excel_beneficio'),
    path('upload-folha/', views.upload_excel_folha, name='upload_excel_folha'),
    path('delete-comp/', views.delete_comp_view, name='delete_comp'),
]

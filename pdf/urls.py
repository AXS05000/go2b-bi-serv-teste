from django.urls import path

from . import views

urlpatterns = [
    path('sf/', views.selecionar_funcionario, name='selecionar_funcionario'),
    path('sf2/', views.selecionar_funcionario2, name='selecionar_funcionario2'),
    path('gerar-pdf/<int:codigo_fc>/<int:comp>/', views.gerar_pdf_direto, name='gerar_pdf_direto'),
    path('gerar-pdf-2/<int:codigo_fc>/<int:comp>/', views.gerar_pdf_direto2, name='gerar_pdf_direto2'),
    path('upload/', views.upload_excel, name='upload_excel'),
    path('upload-pdf-banco/', views.upload_file_banco_pdf, name='upload_banco_pdf'),
    path('upload-bene/', views.upload_excel_bene, name='upload_excel_beneficio'),
    path('upload-folha/', views.upload_excel_folha, name='upload_excel_folha'),
    path('delete-comp/', views.delete_comp_view, name='delete_comp'),
    path('download/', views.download_file, name='download_file'),
    path('aut/<str:competencia>/<str:autenticacao>/', views.download_file_url, name='download_file_url'),
    path('upload-bet/', views.upload_file_bet, name='upload_file_bet'),
    path('upload-bet-itau/', views.upload_file_bet_itau, name='upload_file_bet_itau'),
    path('processar-arquivos/', views.process_files_view),
    path('processar-arquivos-bradesco/', views.process_files_view_bradesco),
    path('processar-arquivos-itau/', views.process_files_view_itau),
    path('gerar-pdf/', views.gerar_pdf_competencia, name='gerar_pdf_competencia'),
    path('otimizar/', views.otimizar_referencias, name='otimizar'),
    path('upload-pagamentos-mala-direta/', views.upload_pagamentos_mala_direta, name='upload_pagamentos_mala_direta'),
   

]

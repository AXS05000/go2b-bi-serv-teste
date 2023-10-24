from django.contrib import admin

from .models import (Arquivo, Beneficios_Mala, Folha_de_Ponto, Funcionario,
                     Pagamentos)

admin.site.register(Funcionario)

admin.site.register(Beneficios_Mala)

admin.site.register(Folha_de_Ponto)

admin.site.register(Arquivo)

admin.site.register(Pagamentos)

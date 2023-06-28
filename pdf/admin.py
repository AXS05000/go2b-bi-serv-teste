from django.contrib import admin

from .models import Beneficios_Mala, Folha_de_Ponto, Funcionario

admin.site.register(Funcionario)

admin.site.register(Beneficios_Mala)

admin.site.register(Folha_de_Ponto)

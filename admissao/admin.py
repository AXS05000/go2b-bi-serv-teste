from django.contrib import admin

from .models import (Base, ClienteGI, Collaborator, ContractTemplate,
                     Departamento, Turno)

admin.site.register(ContractTemplate)

admin.site.register(Collaborator)

admin.site.register(Base)

admin.site.register(ClienteGI)

admin.site.register(Departamento)

admin.site.register(Turno)

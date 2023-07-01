from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from usuarios.views import handler404

handler404 = 'usuarios.views.handler404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pdf.urls')),
    path('', include('admissao.urls')),
    path('', include('usuarios.urls')),
    path('', include('notas.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

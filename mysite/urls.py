"""
URL configuration principal para mysite project.
Este archivo es un fallback - django-tenants usará automáticamente
urls_public.py o urls_tenant.py según el contexto.
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def root_info(request):
    return HttpResponse("""
    <h1>Sistema Financiero Multi-Tenant</h1>
    <p>Error: No se pudo determinar el esquema.</p>
    <p>Asegúrate de acceder mediante el dominio correcto.</p>
    """)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_info, name='root_info'),
]

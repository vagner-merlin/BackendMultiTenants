"""
URLs para el esquema público (compartido entre todos los tenants)
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def public_home(request):
    return JsonResponse({
        'mensaje': 'Esquema Público - Gestión de Institutos',
        'tipo': 'public_schema',
        'apis_disponibles': [
            '/shared/api/institutos/',
            '/shared/api/dominios/'
        ]
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shared/', include('app_shared_Manager.urls_shared')),
    path('', public_home, name='public-home'),
]

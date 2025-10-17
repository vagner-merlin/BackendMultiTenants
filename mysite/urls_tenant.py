"""
URLs para cada tenant (específicas por instituto)
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

def tenant_home(request):
    return JsonResponse({
        'mensaje': f'Panel del Instituto: {request.tenant.nombre}',
        'tipo': 'tenant_schema',
        'instituto': {
            'nombre': request.tenant.nombre,
            'razon_social': request.tenant.razon_social,
            'email': request.tenant.email_contacto
        },
        'apis_disponibles': [
            '/api/usuarios/',
            '/api/usuarios/stats/',
        ]
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tenant_home, name='tenant-home'),
    path('', include('app_tenant_User.urls_tenant')),  # Incluir APIs de usuario
]

# Servir archivos de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

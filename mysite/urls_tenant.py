"""
URLs para cada TENANT (Instituto Financiero Individual)
Cada instituto tiene su propio admin y funcionalidades
Acceso: http://banco-ejemplo.localhost:8000/
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def instituto_dashboard(request):
    return HttpResponse(f"""
    <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px;">
        <h1 style="color: #2c3e50;">🏛️ {request.tenant.nombre}</h1>
        <div style="background: #ecf0f1; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h2>Portal del Instituto Financiero</h2>
            <p><strong>Razón Social:</strong> {request.tenant.razon_social}</p>
            <p><strong>Contacto:</strong> {request.tenant.numero_contacto}</p>
            <p><strong>Schema:</strong> {request.tenant.schema_name}</p>
        </div>
        
        <div style="background: #e74c3c; color: white; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <h3>🎯 Módulos del Instituto:</h3>
            <ul>
                <li><a href="/admin/" style="color: white;"><strong>Admin del Instituto</strong></a> - Gestión específica</li>
                <li><strong>Sistema de Créditos</strong> - Gestión de préstamos y créditos</li>
                <li><strong>Usuarios del Instituto</strong> - Empleados y clientes</li>
                <li><strong>Configuraciones</strong> - Parámetros específicos</li>
            </ul>
        </div>
        
        <div style="background: #f39c12; color: white; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <h3>📊 Apps Disponibles:</h3>
            <p>• tenat_apss_Credito - Sistema de créditos</p>
            <p>• tenat_Django_users - Gestión de usuarios</p>
            <p>• tenat_Enums - Configuraciones y enumeraciones</p>
        </div>
    </div>
    """)

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin específico del INSTITUTO
    path('', instituto_dashboard, name='instituto_dashboard'),
    # Aquí agregarás más URLs específicas del instituto:
    # path('api/creditos/', include('tenat_apss_Credito.urls')),
    # path('usuarios/', include('tenat_Django_users.urls')),
    # path('config/', include('tenat_Enums.urls')),
]
"""
URLs para el ESQUEMA PÚBLICO (Administración de Tenants)
Aquí se administran los institutos financieros (tenants)
Acceso: http://127.0.0.1:8000/
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def admin_dashboard(request):
    return HttpResponse("""
    <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px;">
        <h1 style="color: #2c3e50;">🏦 Sistema Financiero - Administración Central</h1>
        <div style="background: #ecf0f1; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h2>Panel de Administración del Esquema Público</h2>
            <p><strong>Función:</strong> Gestionar institutos financieros (tenants)</p>
            <p><strong>URL Actual:</strong> Esquema Público</p>
        </div>
        
        <div style="background: #3498db; color: white; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <h3>🔧 Acciones Disponibles:</h3>
            <ul>
                <li><a href="/admin/" style="color: white;"><strong>Admin del Sistema</strong></a> - Gestionar institutos y dominios</li>
                <li>Crear nuevos institutos financieros</li>
                <li>Configurar dominios para cada instituto</li>
            </ul>
        </div>
        
        <div style="background: #27ae60; color: white; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <h3>📋 Institutos Existentes:</h3>
            <p><strong>banco-ejemplo.localhost:8000</strong> - Banco Ejemplo S.A.</p>
            <p><em>Para acceder al tenant específico, usa el dominio correspondiente</em></p>
        </div>
    </div>
    """)

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin para gestionar TENANTS
    path('', admin_dashboard, name='admin_dashboard'),
]
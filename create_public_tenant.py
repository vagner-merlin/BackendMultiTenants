"""
Script para crear el tenant público necesario para django-tenants
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from app_shared_Manager.models import Instituto, Domain

def create_public_tenant():
    """Crear el tenant público si no existe"""
    try:
        # Verificar si ya existe el tenant público
        public_tenant = Instituto.objects.filter(schema_name='public').first()
        
        if not public_tenant:
            # Crear el tenant público
            public_tenant = Instituto.objects.create(
                schema_name='public',
                nombre='Sistema Público',
                razon_social='Sistema Público de Gestión',
                email_contacto='admin@sistema.com'
            )
            print("✅ Tenant público creado exitosamente")
        else:
            print("✅ Tenant público ya existe")
        
        # Verificar si existe el dominio localhost
        localhost_domain = Domain.objects.filter(domain='localhost').first()
        
        if not localhost_domain:
            # Crear dominio localhost para el tenant público
            Domain.objects.create(
                tenant=public_tenant,
                domain='localhost',
                is_primary=True
            )
            print("✅ Dominio localhost creado exitosamente")
        else:
            print("✅ Dominio localhost ya existe")
            
        # Crear dominio para 127.0.0.1 también
        local_ip_domain = Domain.objects.filter(domain='127.0.0.1').first()
        
        if not local_ip_domain:
            Domain.objects.create(
                tenant=public_tenant,
                domain='127.0.0.1',
                is_primary=False
            )
            print("✅ Dominio 127.0.0.1 creado exitosamente")
        else:
            print("✅ Dominio 127.0.0.1 ya existe")
            
    except Exception as e:
        print(f"❌ Error al crear tenant público: {e}")

if __name__ == '__main__':
    create_public_tenant()

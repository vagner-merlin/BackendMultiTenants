#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    django.setup()
    
    from shared_Institucion.models import Instituto, Domain
    from django_tenants.utils import get_public_schema_name
    
    # Crear dominio para el esquema público
    from django_tenants.models import TenantMixin
    
    # Crear un tenant especial para el esquema público
    public_tenant = Instituto.objects.get_or_create(
        schema_name=get_public_schema_name(),
        defaults={
            'nombre': 'Administración Central',
            'razon_social': 'Sistema Financiero Central',
            'numero_contacto': '+000000000',
        }
    )[0]
    
    # Crear dominios para acceder al esquema público
    domains_to_create = [
        'localhost:8000',
        '127.0.0.1:8000',
        'admin.localhost:8000',
    ]
    
    for domain_name in domains_to_create:
        domain, created = Domain.objects.get_or_create(
            domain=domain_name,
            defaults={
                'tenant': public_tenant,
                'is_primary': domain_name == 'localhost:8000'
            }
        )
        if created:
            print(f"Dominio creado: {domain_name}")
        else:
            print(f"Dominio ya existe: {domain_name}")
    
    print("¡Configuración de dominios completada!")
    print("\nAhora puedes acceder:")
    print("- Esquema público: http://localhost:8000/admin/")
    print("- Tenant específico: http://banco-ejemplo.localhost:8000/admin/")
#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    django.setup()
    
    from shared_Institucion.models import Instituto, Domain
    
    # Crear el primer instituto
    instituto = Instituto.objects.create(
        schema_name='banco_ejemplo',
        nombre='Banco Ejemplo',
        razon_social='Banco Ejemplo S.A.',
        numero_contacto='+1234567890',
        logo_url='https://ejemplo.com/logo.png'
    )
    
    # Crear el dominio para el instituto
    domain = Domain.objects.create(
        domain='banco-ejemplo.localhost',
        tenant=instituto,
        is_primary=True
    )
    
    print(f"Instituto creado: {instituto.nombre}")
    print(f"Schema: {instituto.schema_name}")
    print(f"Dominio: {domain.domain}")
    print("¡Tenant creado exitosamente!")
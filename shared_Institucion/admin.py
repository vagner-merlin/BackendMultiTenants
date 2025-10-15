from django.contrib import admin
from .models import Instituto, Domain

@admin.register(Instituto)
class InstitutoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'razon_social', 'numero_contacto', 'schema_name', 'fecha_registro')
    list_filter = ('fecha_registro',)
    search_fields = ('nombre', 'razon_social', 'schema_name')
    readonly_fields = ('fecha_registro', 'schema_name')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'razon_social', 'numero_contacto')
        }),
        ('Configuración Técnica', {
            'fields': ('schema_name', 'fecha_registro'),
            'classes': ('collapse',)
        }),
        ('Branding', {
            'fields': ('logo_url',),
            'classes': ('collapse',)
        })
    )

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'tenant', 'is_primary')
    list_filter = ('is_primary',)
    search_fields = ('domain', 'tenant__nombre')

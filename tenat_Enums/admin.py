from django.contrib import admin
from .models import PlanTenant, EstadoSaasTenant, TemaTenant

@admin.register(PlanTenant)
class PlanTenantAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo_plan', 'limite_usuarios', 'limite_creditos', 'activo']
    list_filter = ['tipo_plan', 'activo']
    search_fields = ['nombre', 'descripcion']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'activo')
        }),
        ('Configuración del Plan', {
            'fields': ('tipo_plan', 'limite_usuarios', 'limite_creditos')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(EstadoSaasTenant)
class EstadoSaasTenantAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'estado', 'fecha_vencimiento_prueba', 'activo']
    list_filter = ['estado', 'activo']
    search_fields = ['nombre', 'descripcion']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'activo')
        }),
        ('Estado SaaS', {
            'fields': ('estado', 'fecha_vencimiento_prueba')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(TemaTenant)
class TemaTenantAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tema', 'color_primario', 'color_secundario', 'activo']
    list_filter = ['tema', 'activo']
    search_fields = ['nombre', 'descripcion']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'activo')
        }),
        ('Configuración Visual', {
            'fields': ('tema', 'color_primario', 'color_secundario')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

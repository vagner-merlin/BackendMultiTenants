from django.contrib import admin
from .models import PagoSuscripciones, AppSuscripciones

class AppSuscripcionesInline(admin.TabularInline):
    model = AppSuscripciones
    extra = 1
    fields = ['enum_plan', 'enum_estado_saas', 'fecha_inicio', 'fecha_final']

@admin.register(PagoSuscripciones)
class PagoSuscripcionesAdmin(admin.ModelAdmin):
    list_display = [
        'instituto', 'fecha_pago', 'monto_pagado', 'tiempo_cubierto'
    ]
    list_filter = ['fecha_pago']
    search_fields = ['instituto__nombre', 'id_transaccion_externo']
    inlines = [AppSuscripcionesInline]
    
    fieldsets = (
        ('Información del Instituto', {
            'fields': ('instituto',)
        }),
        ('Detalles del Pago', {
            'fields': ('fecha_pago', 'monto_pagado', 'tiempo_cubierto', 'id_transaccion_externo')
        })
    )

@admin.register(AppSuscripciones)
class AppSuscripcionesAdmin(admin.ModelAdmin):
    list_display = [
        'get_instituto_nombre', 'enum_plan', 'enum_estado_saas', 
        'fecha_inicio', 'fecha_final'
    ]
    list_filter = ['enum_plan', 'enum_estado_saas', 'fecha_inicio']
    search_fields = ['pago_suscripcion__instituto__nombre']
    
    def get_instituto_nombre(self, obj):
        return obj.pago_suscripcion.instituto.nombre
    get_instituto_nombre.short_description = 'Instituto'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('pago_suscripcion', 'enum_plan')
        }),
        ('Estado y Fechas', {
            'fields': ('enum_estado_saas', 'fecha_inicio', 'fecha_final')
        })
    )

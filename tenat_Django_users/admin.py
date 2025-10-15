from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import AppCustomUser, Custom

class AppCustomUserInline(admin.StackedInline):
    model = AppCustomUser
    can_delete = False
    verbose_name_plural = 'Perfil Custom'
    fields = ['custom', 'foto_perfil_url', 'telefono']

# Extender el admin de User para incluir el perfil custom
class UserAdmin(BaseUserAdmin):
    inlines = (AppCustomUserInline,)

# Re-registrar UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Custom)
class CustomAdmin(admin.ModelAdmin):
    list_display = ['id', 'enum_tema', 'color', 'tipos_letra', 'cantidad_usuarios']
    list_filter = ['enum_tema']
    search_fields = ['color', 'tipos_letra']
    
    def cantidad_usuarios(self, obj):
        return obj.usuarios.count()
    cantidad_usuarios.short_description = 'Usuarios usando este custom'
    
    fieldsets = (
        ('Configuración Visual', {
            'fields': ('enum_tema', 'color', 'tipos_letra')
        }),
    )

@admin.register(AppCustomUser)
class AppCustomUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'nombre_completo', 'get_tema', 'foto_perfil_url', 'telefono']
    list_filter = ['custom__enum_tema']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'telefono']
    
    def get_tema(self, obj):
        return obj.custom.get_enum_tema_display() if obj.custom else "Sin tema"
    get_tema.short_description = 'Tema'
    
    fieldsets = (
        ('Usuario Base', {
            'fields': ('user',)
        }),
        ('Configuración', {
            'fields': ('custom',)
        }),
        ('Información Adicional', {
            'fields': ('foto_perfil_url', 'telefono')
        }),
    )

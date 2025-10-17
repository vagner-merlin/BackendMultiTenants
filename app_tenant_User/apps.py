from django.apps import AppConfig


class AppTenantUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_tenant_User'
    verbose_name = 'Gestión de Usuarios por Tenant'

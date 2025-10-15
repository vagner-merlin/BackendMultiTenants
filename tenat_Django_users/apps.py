from django.apps import AppConfig


class TenatDjangoUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tenat_Django_users'
    
    def ready(self):
        import tenat_Django_users.models  # Importar para registrar las señales

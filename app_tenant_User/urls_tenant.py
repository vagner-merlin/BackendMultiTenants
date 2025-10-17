from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_rest

# Crear router para las APIs de usuario
router = DefaultRouter()
router.register(r'usuarios', api_rest.TenantUserViewSet)

urlpatterns = [
    # API de usuarios (requiere token)
    path('api/', include(router.urls)),
    
    # Rutas adicionales
    path('', include(router.urls)),  # Para acceso directo
]

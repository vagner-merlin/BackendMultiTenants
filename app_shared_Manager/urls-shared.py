from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_rest  # Importar el archivo correcto (api_rest.py)

# Crear router para las APIs
router = DefaultRouter()
router.register(r'institutos', api_rest.InstitutoViewSet)
router.register(r'dominios', api_rest.DomainViewSet)
router.register(r'auth', api_rest.AuthViewSet, basename='auth')  # Agregar auth

urlpatterns = [
    # Incluir todas las rutas del router
    path('api/', include(router.urls)),
    
    # Rutas adicionales si necesitas
    path('', include(router.urls)),  # Para acceso directo sin 'api/'
]

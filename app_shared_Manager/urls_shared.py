from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_rest

# Crear router para las APIs
router = DefaultRouter()
router.register(r'institutos', api_rest.InstitutoViewSet)
router.register(r'dominios', api_rest.DomainViewSet)
router.register(r'auth', api_rest.AuthViewSet, basename='auth')

urlpatterns = [
    # Incluir todas las rutas del router
    path('api/', include(router.urls)),
    
    # Rutas adicionales si necesitas
    path('', include(router.urls)),  # Para acceso directo sin 'api/'
]

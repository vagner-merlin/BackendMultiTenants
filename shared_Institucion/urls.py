from django.urls import path
from . import views

app_name = 'shared_institucion'

urlpatterns = [
    # CRUD de Institutos
    path('institutos/', views.InstitutoListCreateView.as_view(), name='instituto-list-create'),
    path('institutos/<int:pk>/', views.InstitutoDetailView.as_view(), name='instituto-detail'),
    
    # Gestión de dominios
    path('institutos/<int:instituto_id>/dominios/', views.add_domain_to_instituto, name='add-domain'),
    
    # Verificaciones de disponibilidad
    path('check-domain/', views.check_domain_availability, name='check-domain'),
    path('check-schema/', views.check_schema_availability, name='check-schema'),
]
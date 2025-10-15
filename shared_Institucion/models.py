from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Instituto(TenantMixin):
    
    razon_social = models.CharField(max_length=200, verbose_name="Razón Social")
    numero_contacto = models.CharField(max_length=20, verbose_name="Número de Contacto")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Instituto")
    logo_url = models.URLField(blank=True, null=True, verbose_name="URL del Logo")
   
    auto_create_schema = True
    auto_drop_schema = True
    
    class Meta:
        verbose_name = "Instituto Financiero"
        verbose_name_plural = "Institutos Financieros"
    
    def __str__(self):
        return self.nombre

class Domain(DomainMixin):
    
    pass
 
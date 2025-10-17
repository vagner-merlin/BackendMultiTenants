from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Instituto(TenantMixin):
    razon_social = models.CharField(max_length=200, verbose_name="Razón Social")
    email_contacto = models.EmailField(verbose_name="Email de Contacto")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Instituto")
    logo_url = models.URLField(blank=True, null=True, verbose_name="URL del Logo")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    auto_create_schema = True
    auto_drop_schema = True

    class Meta:
        verbose_name = "Instituto"
        verbose_name_plural = "Institutos"

    def __str__(self):
        return self.nombre


class Domain(DomainMixin):
    class Meta:
        verbose_name = "Dominio"
        verbose_name_plural = "Dominios"

    def __str__(self):
        return self.domain

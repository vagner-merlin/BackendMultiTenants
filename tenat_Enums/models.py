from django.db import models
from .enums import (
    ENUM_PLAN_CHOICES, 
    ENUM_ESTADO_SAAS_CHOICES, 
    ENUM_TEMA_CHOICES, 
    ENUM_ESTADO_CREDITO_CHOICES,
    LICENCIA_ON_PREMISE_CHOICES,
    DEFAULT_PLAN,
    DEFAULT_ESTADO_SAAS,
    DEFAULT_TEMA
)

class ConfiguracionEnum(models.Model):
    """
    Modelo base para configuraciones de enumeraciones por tenant
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre de Configuración")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    
    class Meta:
        verbose_name = "Configuración de Enum"
        verbose_name_plural = "Configuraciones de Enums"
        abstract = True

class PlanTenant(ConfiguracionEnum):
    """
    Configuración del plan para el tenant actual
    """
    tipo_plan = models.CharField(
        max_length=20,
        choices=ENUM_PLAN_CHOICES,
        default=DEFAULT_PLAN,  # Por defecto 'gratis'
        verbose_name="Tipo de Plan"
    )
    limite_usuarios = models.IntegerField(default=5, verbose_name="Límite de Usuarios")
    limite_creditos = models.IntegerField(default=10, verbose_name="Límite de Créditos Mensuales")
    
    class Meta:
        verbose_name = "Plan del Tenant"
        verbose_name_plural = "Planes del Tenant"
    
    def __str__(self):
        return f"Plan {self.get_tipo_plan_display()}"

class EstadoSaasTenant(ConfiguracionEnum):
    """
    Estado SaaS del tenant actual
    """
    estado = models.CharField(
        max_length=20,
        choices=ENUM_ESTADO_SAAS_CHOICES,
        default=DEFAULT_ESTADO_SAAS,  # Por defecto 'en_prueba'
        verbose_name="Estado SaaS"
    )
    fecha_vencimiento_prueba = models.DateTimeField(
        null=True, blank=True,
        verbose_name="Fecha de Vencimiento de Prueba"
    )
    
    class Meta:
        verbose_name = "Estado SaaS del Tenant"
        verbose_name_plural = "Estados SaaS del Tenant"
    
    def __str__(self):
        return f"Estado: {self.get_estado_display()}"

class TemaTenant(ConfiguracionEnum):
    """
    Configuración de tema para el tenant
    """
    tema = models.CharField(
        max_length=20,
        choices=ENUM_TEMA_CHOICES,
        default=DEFAULT_TEMA,  # Por defecto 'automatico'
        verbose_name="Tema"
    )
    color_primario = models.CharField(
        max_length=7, 
        default="#3498db",
        verbose_name="Color Primario (HEX)"
    )
    color_secundario = models.CharField(
        max_length=7, 
        default="#2c3e50",
        verbose_name="Color Secundario (HEX)"
    )
    
    class Meta:
        verbose_name = "Tema del Tenant"
        verbose_name_plural = "Temas del Tenant"
    
    def __str__(self):
        return f"Tema: {self.get_tema_display()}"

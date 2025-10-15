from django.db import models
from shared_Institucion.models import Instituto
from tenat_Enums.enums import ENUM_PLAN_CHOICES, ENUM_ESTADO_SAAS_CHOICES, DEFAULT_PLAN, DEFAULT_ESTADO_SAAS

class PagoSuscripciones(models.Model):
   
    instituto = models.OneToOneField(
        Instituto, 
        on_delete=models.CASCADE, 
        related_name='pago_suscripcion',
        verbose_name="Instituto"
    )
    
   
    fecha_pago = models.DateTimeField(verbose_name="Fecha de Pago")
    monto_pagado = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Monto Pagado"
    )
    tiempo_cubierto = models.IntegerField(verbose_name="Tiempo Cubierto")
    id_transaccion_externo = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name="ID Transacción Externo"
    )
    
    class Meta:
        verbose_name = "Pago de Suscripción"
        verbose_name_plural = "Pagos de Suscripciones"
    
    def __str__(self):
        return f"Pago {self.instituto.nombre}"

class AppSuscripciones(models.Model):
    
    pago_suscripcion = models.ForeignKey(
        PagoSuscripciones,
        on_delete=models.CASCADE,
        related_name='apps_contratadas',
        verbose_name="Pago de Suscripción"
    )
    
    enum_plan = models.CharField(
        max_length=20,
        choices=ENUM_PLAN_CHOICES,
        default=DEFAULT_PLAN,
        verbose_name="Plan"
    )
    enum_estado_saas = models.CharField(
        max_length=20,
        choices=ENUM_ESTADO_SAAS_CHOICES,
        default=DEFAULT_ESTADO_SAAS,
        verbose_name="Estado SaaS"
    )
    fecha_inicio = models.DateTimeField(verbose_name="Fecha de Inicio")
    fecha_final = models.DateTimeField(verbose_name="Fecha Final")
    
    class Meta:
        verbose_name = "App de Suscripción"
        verbose_name_plural = "Apps de Suscripciones"
    
    def __str__(self):
        return f"App - {self.pago_suscripcion.instituto.nombre}"

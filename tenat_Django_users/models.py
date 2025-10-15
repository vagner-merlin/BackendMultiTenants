from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from tenat_Enums.enums import ENUM_TEMA_CHOICES, DEFAULT_TEMA

class Custom(models.Model):
    
    color = models.CharField(
        max_length=7, 
        verbose_name="Color",
        help_text="Color en formato HEX (ej: #3498db)"
    )
    tipos_letra = models.CharField(
        max_length=50,
        verbose_name="Tipos de Letra"
    )
    enum_tema = models.CharField(
        max_length=20,
        choices=ENUM_TEMA_CHOICES,
        default=DEFAULT_TEMA,
        verbose_name="Tema"
    )
    
    class Meta:
        verbose_name = "Configuración Custom"
        verbose_name_plural = "Configuraciones Custom"
    
    def __str__(self):
        return f"Custom {self.get_enum_tema_display()} - {self.color}"


class AppCustomUser(models.Model):
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='custom_profile',
        verbose_name="Usuario"
    )

    custom = models.ForeignKey(
        Custom,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios',
        verbose_name="Configuración Custom"
    )

    foto_perfil_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Foto de Perfil URL"
    )

    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Teléfono"
    )
    
    class Meta:
        verbose_name = "Perfil de Usuario Custom"
        verbose_name_plural = "Perfiles de Usuarios Custom"
    
    def __str__(self):
        return f"Perfil de {self.user.username}"
    
    @property
    def nombre_completo(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username

# Señal para crear automáticamente el perfil custom cuando se crea un usuario
@receiver(post_save, sender=User)
def crear_perfil_custom(sender, instance, created, **kwargs):
    if created:
        AppCustomUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def guardar_perfil_custom(sender, instance, **kwargs):
    if hasattr(instance, 'custom_profile'):
        instance.custom_profile.save()

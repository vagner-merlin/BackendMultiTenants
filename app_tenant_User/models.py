from django.db import models
from django.core.validators import FileExtensionValidator


class TenantUser(models.Model):
    """Modelo simple de usuario para cada tenant"""

    username = models.CharField(max_length=150, unique=True, verbose_name="Nombre de Usuario")
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=30, verbose_name="Nombre")
    last_name = models.CharField(max_length=150, verbose_name="Apellidos")

    # Campos adicionales del perfil
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name="Fecha de Nacimiento")

    # Foto de perfil
    foto_perfil = models.ImageField(
        upload_to="perfiles/",
        blank=True,
        null=True,
        verbose_name="Foto de Perfil",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif"])],
    )

    # Campos profesionales
    cargo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cargo")
    departamento = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Departamento"
    )
    fecha_ingreso = models.DateField(
        blank=True, null=True, verbose_name="Fecha de Ingreso"
    )

    # Campos de estado
    activo = models.BooleanField(default=True, verbose_name="Usuario Activo")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Usuario del Tenant"
        verbose_name_plural = "Usuarios del Tenant"
        ordering = ["-fecha_registro"]

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

    def get_full_name(self):
        """Retorna nombre completo del usuario"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    @property
    def tiene_foto_perfil(self):
        """Verifica si el usuario tiene foto de perfil"""
        return bool(self.foto_perfil)

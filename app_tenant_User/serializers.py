from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, TenantUser


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer para operaciones generales del usuario"""
    
    nombre_completo = serializers.CharField(source='get_full_name', read_only=True)
    tiene_foto = serializers.BooleanField(source='tiene_foto_perfil', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'nombre_completo',
            'telefono',
            'direccion',
            'fecha_nacimiento',
            'foto_perfil',
            'tiene_foto',
            'cargo',
            'departamento',
            'fecha_ingreso',
            'activo',
            'fecha_registro',
            'fecha_actualizacion',
            'is_staff',
            'is_active'
        ]
        read_only_fields = ['id', 'fecha_registro', 'fecha_actualizacion', 'nombre_completo', 'tiene_foto']


class UserProfileCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear usuarios"""
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'username',
            'email',
            'password',
            'password_confirm',
            'first_name',
            'last_name',
            'telefono',
            'direccion',
            'fecha_nacimiento',
            'foto_perfil',
            'cargo',
            'departamento',
            'fecha_ingreso'
        ]

    def validate(self, attrs):
        """Validar que las contraseñas coincidan"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return attrs

    def create(self, validated_data):
        """Crear usuario con contraseña encriptada"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = UserProfile.objects.create_user(
            password=password,
            **validated_data
        )
        return user


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualizar usuarios (sin contraseña)"""
    
    class Meta:
        model = UserProfile
        fields = [
            'email',
            'first_name',
            'last_name',
            'telefono',
            'direccion',
            'fecha_nacimiento',
            'foto_perfil',
            'cargo',
            'departamento',
            'fecha_ingreso',
            'activo'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para cambiar contraseña"""
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Las nuevas contraseñas no coinciden")
        return attrs


class TenantUserSerializer(serializers.ModelSerializer):
    """Serializer CRUD completo para usuarios del tenant"""
    
    nombre_completo = serializers.CharField(source='get_full_name', read_only=True)
    tiene_foto = serializers.BooleanField(source='tiene_foto_perfil', read_only=True)
    
    class Meta:
        model = TenantUser
        fields = [
            'id',
            'username',
            'email', 
            'first_name',
            'last_name',
            'nombre_completo',
            'telefono',
            'direccion',
            'fecha_nacimiento',
            'foto_perfil',
            'tiene_foto',
            'cargo',
            'departamento',
            'fecha_ingreso',
            'activo',
            'fecha_registro',
            'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'fecha_registro', 'fecha_actualizacion', 'nombre_completo', 'tiene_foto']

    def validate_email(self, value):
        """Validar email único en el tenant"""
        instance = getattr(self, 'instance', None)
        if instance and instance.email == value:
            return value
        
        if TenantUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ya existe un usuario con este email")
        return value

    def validate_username(self, value):
        """Validar username único en el tenant"""
        instance = getattr(self, 'instance', None)
        if instance and instance.username == value:
            return value
            
        if TenantUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ya existe un usuario con este username")
        return value

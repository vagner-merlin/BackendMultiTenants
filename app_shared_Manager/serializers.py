from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.authtoken.models import Token
from .models import Instituto, Domain


class InstitutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instituto
        fields = [
            'id',
            'schema_name',
            'razon_social', 
            'email_contacto',
            'fecha_registro',
            'nombre',
            'logo_url',
            'telefono',
            'direccion',
            'activo'
        ]
        read_only_fields = ['id', 'fecha_registro']

    def validate_schema_name(self, value):
        """Validar que el schema_name sea único y tenga formato correcto"""
        if not value.islower():
            raise serializers.ValidationError("El schema_name debe estar en minúsculas")
        if Instituto.objects.filter(schema_name=value).exists():
            raise serializers.ValidationError("Ya existe un instituto con este schema_name")
        return value


class DomainSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source='tenant.nombre', read_only=True)
    
    class Meta:
        model = Domain
        fields = [
            'id',
            'domain',
            'tenant',
            'tenant_name',
            'is_primary'
        ]

    def validate_domain(self, value):
        """Validar que el dominio sea único"""
        if Domain.objects.filter(domain=value).exists():
            raise serializers.ValidationError("Ya existe este dominio")
        return value


class InstitutoCompleteCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear instituto completo con dominio y administrador"""
    
    # Datos del Instituto
    razon_social = serializers.CharField(max_length=200)
    email_contacto = serializers.EmailField()
    nombre = serializers.CharField(max_length=100)
    telefono = serializers.CharField(max_length=20, required=False, allow_blank=True)
    
    # Datos del Dominio
    domain_name = serializers.CharField(
        write_only=True, 
        help_text="Nombre del dominio de trabajo (ej: empresa1.localhost)"
    )
    
    # Datos del Administrador
    admin_username = serializers.CharField(
        write_only=True,
        help_text="Nombre de usuario del administrador"
    )
    admin_first_name = serializers.CharField(
        write_only=True,
        help_text="Nombre del administrador"
    )
    admin_last_name = serializers.CharField(
        write_only=True,
        help_text="Apellido del administrador"
    )
    admin_email = serializers.EmailField(
        write_only=True,
        help_text="Email del administrador"
    )
    admin_password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="Contraseña del administrador (mínimo 8 caracteres)"
    )
    
    # Campos de respuesta
    domain_created = serializers.CharField(read_only=True)
    admin_created = serializers.CharField(read_only=True)
    admin_token = serializers.CharField(read_only=True)  # Nuevo campo para token
    
    class Meta:
        model = Instituto
        fields = [
            # Datos del Instituto
            'schema_name',
            'razon_social',
            'email_contacto',
            'nombre',
            'telefono',
            
            # Datos del Dominio (write_only)
            'domain_name',
            
            # Datos del Administrador (write_only)
            'admin_username',
            'admin_first_name',
            'admin_last_name',
            'admin_email',
            'admin_password',
            
            # Campos de respuesta (read_only)
            'id',
            'fecha_registro',
            'domain_created',
            'admin_created',
            'admin_token'  # Nuevo campo
        ]
        read_only_fields = ['id', 'fecha_registro', 'domain_created', 'admin_created', 'admin_token']

    def validate_schema_name(self, value):
        """Validar que el schema_name sea único y tenga formato correcto"""
        if not value.islower():
            raise serializers.ValidationError("El schema_name debe estar en minúsculas")
        if Instituto.objects.filter(schema_name=value).exists():
            raise serializers.ValidationError("Ya existe un instituto con este schema_name")
        return value

    def validate_domain_name(self, value):
        """Validar que el dominio sea único"""
        if Domain.objects.filter(domain=value).exists():
            raise serializers.ValidationError("Ya existe este dominio")
        return value

    def validate_admin_username(self, value):
        """Validar que el username del admin sea único en el esquema público"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ya existe este nombre de usuario")
        return value

    def validate_admin_email(self, value):
        """Validar que el email del admin sea único en el esquema público"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ya existe este email de administrador")
        return value

    @transaction.atomic
    def create(self, validated_data):
        """Crear instituto, dominio y usuario administrador con token"""
        
        # Extraer datos del dominio y administrador
        domain_name = validated_data.pop('domain_name')
        admin_username = validated_data.pop('admin_username')
        admin_first_name = validated_data.pop('admin_first_name')
        admin_last_name = validated_data.pop('admin_last_name')
        admin_email = validated_data.pop('admin_email')
        admin_password = validated_data.pop('admin_password')
        
        try:
            # 1. Crear el Instituto
            instituto = Instituto.objects.create(**validated_data)
            
            # 2. Crear el Dominio asociado
            domain = Domain.objects.create(
                tenant=instituto,
                domain=domain_name,
                is_primary=True
            )
            
            # 3. Crear el Usuario Administrador en el esquema público
            admin_user = User.objects.create_user(
                username=admin_username,
                email=admin_email,
                password=admin_password,
                first_name=admin_first_name,
                last_name=admin_last_name,
                is_staff=True,  # Por defecto es staff
                is_active=True
            )
            
            # 4. Crear token para el administrador
            token, created = Token.objects.get_or_create(user=admin_user)
            
            # Agregar información de lo que se creó para la respuesta
            instituto.domain_created = domain_name
            instituto.admin_created = f"{admin_first_name} {admin_last_name} ({admin_username})"
            instituto.admin_token = token.key
            
            return instituto
            
        except Exception as e:
            # Si algo falla, la transacción se revierte automáticamente
            raise serializers.ValidationError(f"Error al crear instituto completo: {str(e)}")


class InstitutoCreateSerializer(serializers.ModelSerializer):
    """Serializer simple para crear solo instituto con dominio"""
    domain_name = serializers.CharField(write_only=True, help_text="Nombre del dominio (ej: instituto1.localhost)")
    
    class Meta:
        model = Instituto
        fields = [
            'schema_name',
            'razon_social',
            'email_contacto', 
            'nombre',
            'logo_url',
            'telefono',
            'direccion',
            'domain_name'
        ]

    def validate_schema_name(self, value):
        """Validar que el schema_name sea único y tenga formato correcto"""
        if not value.islower():
            raise serializers.ValidationError("El schema_name debe estar en minúsculas")
        if Instituto.objects.filter(schema_name=value).exists():
            raise serializers.ValidationError("Ya existe un instituto con este schema_name")
        return value

    def validate_domain_name(self, value):
        """Validar que el dominio sea único"""
        if Domain.objects.filter(domain=value).exists():
            raise serializers.ValidationError("Ya existe este dominio")
        return value

    def create(self, validated_data):
        domain_name = validated_data.pop('domain_name')
        
        # Crear el instituto
        instituto = Instituto.objects.create(**validated_data)
        
        # Crear el dominio asociado
        Domain.objects.create(
            tenant=instituto,
            domain=domain_name,
            is_primary=True
        )
        
        return instituto


class LoginSerializer(serializers.Serializer):
    """Serializer para login de usuario"""
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            try:
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    raise serializers.ValidationError('Credenciales inválidas')
                if not user.is_active:
                    raise serializers.ValidationError('Usuario inactivo')
                attrs['user'] = user
            except User.DoesNotExist:
                raise serializers.ValidationError('Usuario no encontrado')
        else:
            raise serializers.ValidationError('Email y contraseña son requeridos')
            
        return attrs

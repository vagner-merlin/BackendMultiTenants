from rest_framework import serializers
from .models import Instituto, Domain

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['domain', 'is_primary']

class InstitutoSerializer(serializers.ModelSerializer):
    domains = DomainSerializer(many=True, read_only=True)
    domain_name = serializers.CharField(write_only=True, help_text="Dominio principal del instituto")
    
    class Meta:
        model = Instituto
        fields = ['id', 'name', 'schema_name', 'created_on', 'domains', 'domain_name']
        read_only_fields = ['id', 'created_on', 'domains']
    
    def validate_schema_name(self, value):
        """Validar que el schema_name sea válido"""
        if not value.islower():
            raise serializers.ValidationError("El schema_name debe estar en minúsculas")
        if ' ' in value:
            raise serializers.ValidationError("El schema_name no puede contener espacios")
        return value
    
    def validate_domain_name(self, value):
        """Validar que el dominio sea válido"""
        if Domain.objects.filter(domain=value).exists():
            raise serializers.ValidationError("Este dominio ya existe")
        return value
    
    def create(self, validated_data):
        domain_name = validated_data.pop('domain_name')
        
        # Crear instituto
        instituto = Instituto.objects.create(**validated_data)
        
        # Crear dominio principal
        Domain.objects.create(
            domain=domain_name,
            tenant=instituto,
            is_primary=True
        )
        
        return instituto

class InstitutoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado"""
    primary_domain = serializers.SerializerMethodField()
    
    class Meta:
        model = Instituto
        fields = ['id', 'name', 'schema_name', 'created_on', 'primary_domain']
    
    def get_primary_domain(self, obj):
        primary_domain = obj.domains.filter(is_primary=True).first()
        return primary_domain.domain if primary_domain else None
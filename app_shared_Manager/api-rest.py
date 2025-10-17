from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Instituto, Domain
from .serializers import (
    InstitutoSerializer, 
    DomainSerializer, 
    InstitutoCreateSerializer
)


class InstitutoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar operaciones CRUD de Instituto
    """
    queryset = Instituto.objects.all()
    serializer_class = InstitutoSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return InstitutoCreateSerializer
        return InstitutoSerializer

    @action(detail=True, methods=['get'])
    def dominios(self, request, pk=None):
        """Obtener todos los dominios de un instituto específico"""
        instituto = self.get_object()
        dominios = Domain.objects.filter(tenant=instituto)
        serializer = DomainSerializer(dominios, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def activar(self, request, pk=None):
        """Activar un instituto"""
        instituto = self.get_object()
        instituto.activo = True
        instituto.save()
        return Response({'status': 'Instituto activado'})

    @action(detail=True, methods=['post'])  
    def desactivar(self, request, pk=None):
        """Desactivar un instituto"""
        instituto = self.get_object()
        instituto.activo = False
        instituto.save()
        return Response({'status': 'Instituto desactivado'})


class DomainViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar operaciones CRUD de Domain
    """
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer

    def create(self, request, *args, **kwargs):
        """Crear un nuevo dominio"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Verificar que el tenant existe
        tenant_id = serializer.validated_data['tenant'].id
        instituto = get_object_or_404(Instituto, id=tenant_id)
        
        domain = serializer.save()
        return Response(
            DomainSerializer(domain).data, 
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def set_primary(self, request, pk=None):
        """Establecer un dominio como primario"""
        domain = self.get_object()
        
        # Desactivar otros dominios primarios del mismo tenant
        Domain.objects.filter(
            tenant=domain.tenant, 
            is_primary=True
        ).update(is_primary=False)
        
        # Activar este como primario
        domain.is_primary = True
        domain.save()
        
        return Response({'status': 'Dominio establecido como primario'})

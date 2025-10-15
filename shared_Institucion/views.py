from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db import transaction
from .models import Instituto, Domain
from .serializers import InstitutoSerializer, InstitutoListSerializer, DomainSerializer

class InstitutoListCreateView(generics.ListCreateAPIView):
    """
    GET: Lista todos los institutos
    POST: Crea un nuevo instituto con su dominio principal
    """
    queryset = Instituto.objects.all()
    permission_classes = [permissions.AllowAny]  # Cambia según tus necesidades
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return InstitutoListSerializer
        return InstitutoSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            with transaction.atomic():
                instituto = serializer.save()
                
                # Retornar la información completa del instituto creado
                response_serializer = InstitutoListSerializer(instituto)
                return Response(
                    {
                        'message': 'Instituto creado exitosamente',
                        'data': response_serializer.data
                    },
                    status=status.HTTP_201_CREATED
                )
        except Exception as e:
            return Response(
                {'error': f'Error al crear instituto: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

class InstitutoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Obtiene detalles de un instituto específico
    PUT/PATCH: Actualiza un instituto
    DELETE: Elimina un instituto
    """
    queryset = Instituto.objects.all()
    serializer_class = InstitutoSerializer
    permission_classes = [permissions.AllowAny]  # Cambia según tus necesidades

@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # Cambia según tus necesidades
def add_domain_to_instituto(request, instituto_id):
    """
    Agregar un dominio adicional a un instituto existente
    """
    try:
        instituto = Instituto.objects.get(id=instituto_id)
    except Instituto.DoesNotExist:
        return Response(
            {'error': 'Instituto no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = DomainSerializer(data=request.data)
    if serializer.is_valid():
        # Verificar que el dominio no exista
        if Domain.objects.filter(domain=serializer.validated_data['domain']).exists():
            return Response(
                {'error': 'Este dominio ya existe'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        domain = serializer.save(tenant=instituto)
        return Response(
            {
                'message': 'Dominio agregado exitosamente',
                'data': DomainSerializer(domain).data
            },
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def check_domain_availability(request):
    """
    Verificar si un dominio está disponible
    """
    domain = request.query_params.get('domain')
    if not domain:
        return Response(
            {'error': 'Parámetro domain requerido'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    exists = Domain.objects.filter(domain=domain).exists()
    return Response({
        'domain': domain,
        'available': not exists,
        'message': 'Dominio disponible' if not exists else 'Dominio ya existe'
    })

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def check_schema_availability(request):
    """
    Verificar si un schema_name está disponible
    """
    schema_name = request.query_params.get('schema_name')
    if not schema_name:
        return Response(
            {'error': 'Parámetro schema_name requerido'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    exists = Instituto.objects.filter(schema_name=schema_name).exists()
    return Response({
        'schema_name': schema_name,
        'available': not exists,
        'message': 'Schema disponible' if not exists else 'Schema ya existe'
    })

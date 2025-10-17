from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .models import TenantUser
from .serializers import TenantUserSerializer


class TenantUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet CRUD completo para usuarios del tenant - Requiere Token
    """
    queryset = TenantUser.objects.all()
    serializer_class = TenantUserSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request, *args, **kwargs):
        """GET /api/usuarios/ - Listar usuarios"""
        queryset = self.get_queryset()
        
        # Filtros opcionales
        activo = request.query_params.get('activo', None)
        if activo is not None:
            queryset = queryset.filter(activo=activo.lower() == 'true')
            
        departamento = request.query_params.get('departamento', None) 
        if departamento:
            queryset = queryset.filter(departamento__icontains=departamento)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'count': queryset.count(),
            'usuarios': serializer.data
        })

    def create(self, request, *args, **kwargs):
        """POST /api/usuarios/ - Crear usuario"""
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'success': True,
                'message': 'Usuario creado exitosamente',
                'usuario': TenantUserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """GET /api/usuarios/{id}/ - Obtener usuario específico"""
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response({
            'success': True,
            'usuario': serializer.data
        })

    def update(self, request, *args, **kwargs):
        """PUT /api/usuarios/{id}/ - Actualizar usuario completo"""
        partial = kwargs.pop('partial', False)
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=partial)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Usuario actualizado exitosamente',
                'usuario': serializer.data
            })
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """PATCH /api/usuarios/{id}/ - Actualizar usuario parcial"""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """DELETE /api/usuarios/{id}/ - Eliminar usuario"""
        user = self.get_object()
        user_data = TenantUserSerializer(user).data
        user.delete()
        
        return Response({
            'success': True,
            'message': f'Usuario {user.get_full_name()} eliminado exitosamente',
            'usuario_eliminado': user_data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """GET /api/usuarios/stats/ - Estadísticas de usuarios"""
        total = TenantUser.objects.count()
        activos = TenantUser.objects.filter(activo=True).count()
        con_foto = TenantUser.objects.exclude(foto_perfil='').count()
        
        return Response({
            'success': True,
            'estadisticas': {
                'total_usuarios': total,
                'usuarios_activos': activos,
                'usuarios_inactivos': total - activos,
                'usuarios_con_foto': con_foto,
                'porcentaje_con_foto': round((con_foto / total * 100) if total > 0 else 0, 2)
            }
        })

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """POST /api/usuarios/{id}/toggle_status/ - Cambiar estado activo/inactivo"""
        user = self.get_object()
        user.activo = not user.activo
        user.save()
        
        return Response({
            'success': True,
            'message': f'Usuario {"activado" if user.activo else "desactivado"} exitosamente',
            'usuario': TenantUserSerializer(user).data
        })

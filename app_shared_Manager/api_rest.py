from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Instituto, Domain
from .serializers import (
    InstitutoSerializer, 
    DomainSerializer, 
    InstitutoCreateSerializer,
    InstitutoCompleteCreateSerializer,
    LoginSerializer
)


class AuthViewSet(viewsets.ViewSet):
    """ViewSet para autenticación"""
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """
        Login de usuario
        POST /shared/api/auth/login/
        """
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Crear o obtener token
            token, created = Token.objects.get_or_create(user=user)
            
            # Buscar si el usuario es admin de algún instituto
            instituto = None
            domain_info = None
            
            try:
                # Buscar instituto por email del administrador
                instituto = Instituto.objects.filter(email_contacto=user.email).first()
                
                if not instituto:
                    # Si no encuentra por email de contacto, buscar por email del admin
                    # Esto es para casos donde el admin_email es diferente al email_contacto
                    institutos = Instituto.objects.all()
                    for inst in institutos:
                        # Verificar si hay un admin user con este email relacionado al instituto
                        if User.objects.filter(email=user.email, is_staff=True).exists():
                            # Podrías implementar una lógica más específica aquí
                            # Por ahora, tomamos el primer instituto si el user es staff
                            instituto = inst
                            break
                
                if instituto:
                    # Obtener dominio principal
                    domain = Domain.objects.filter(tenant=instituto, is_primary=True).first()
                    if domain:
                        domain_info = {
                            'domain': domain.domain,
                            'is_primary': domain.is_primary
                        }
                        
            except Exception as e:
                print(f"Error buscando instituto: {e}")
            
            response_data = {
                'success': True,
                'message': 'Login exitoso',
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_staff': user.is_staff,
                    'is_active': user.is_active
                }
            }
            
            # Si es admin de un instituto, agregar info completa
            if instituto:
                response_data['instituto'] = {
                    'id': instituto.id,
                    'nombre': instituto.nombre,
                    'razon_social': instituto.razon_social,
                    'schema_name': instituto.schema_name,
                    'email_contacto': instituto.email_contacto,
                    'telefono': instituto.telefono,
                    'activo': instituto.activo
                }
                
                # Agregar información del dominio
                if domain_info:
                    response_data['dominio'] = domain_info
                    response_data['urls_acceso'] = {
                        'admin_panel': f"http://{domain_info['domain']}:8000/admin/",
                        'tenant_home': f"http://{domain_info['domain']}:8000/",
                        'api_usuarios': f"http://{domain_info['domain']}:8000/api/usuarios/",
                        'api_stats': f"http://{domain_info['domain']}:8000/api/usuarios/stats/"
                    }
            else:
                response_data['mensaje_adicional'] = 'Usuario no está asociado a ningún instituto'
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """
        Logout de usuario (eliminar token)
        POST /shared/api/auth/logout/
        """
        try:
            request.user.auth_token.delete()
            return Response({
                'success': True,
                'message': 'Logout exitoso'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'error': 'Error al hacer logout'
            }, status=status.HTTP_400_BAD_REQUEST)


class InstitutoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar operaciones CRUD de Instituto
    """
    queryset = Instituto.objects.all()
    serializer_class = InstitutoSerializer

    def get_permissions(self):
        """Permitir crear instituto sin autenticación"""
        if self.action in ['create', 'create_complete']:
            return [AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return InstitutoCreateSerializer
        elif self.action == 'create_complete':
            return InstitutoCompleteCreateSerializer
        return InstitutoSerializer

    @action(detail=False, methods=['post'], url_path='create-complete', permission_classes=[AllowAny])
    def create_complete(self, request):
        """
        Crear instituto completo con dominio y administrador
        POST /shared/api/institutos/create-complete/
        """
        serializer = InstitutoCompleteCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            instituto = serializer.save()
            
            response_data = {
                'success': True,
                'message': 'Instituto creado exitosamente con dominio y administrador',
                'instituto': {
                    'id': instituto.id,
                    'nombre': instituto.nombre,
                    'razon_social': instituto.razon_social,
                    'schema_name': instituto.schema_name,
                    'email_contacto': instituto.email_contacto,
                    'fecha_registro': instituto.fecha_registro
                },
                'domain_created': getattr(instituto, 'domain_created', ''),
                'admin_created': getattr(instituto, 'admin_created', ''),
                'admin_token': getattr(instituto, 'admin_token', ''),
                'urls_acceso': {
                    'admin_panel': f"http://{request.data.get('domain_name')}:8000/admin/",
                    'tenant_home': f"http://{request.data.get('domain_name')}:8000/",
                    'api_usuarios': f"http://{request.data.get('domain_name')}:8000/api/usuarios/",
                    'login': f"http://127.0.0.1:8000/shared/api/auth/login/"
                }
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def dominios(self, request, pk=None):
        """Obtener todos los dominios de un instituto específico"""
        instituto = self.get_object()
        dominios = Domain.objects.filter(tenant=instituto)
        serializer = DomainSerializer(dominios, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def admin_info(self, request, pk=None):
        """Obtener información del administrador del instituto"""
        instituto = self.get_object()
        
        # Buscar el usuario administrador
        try:
            admin_users = User.objects.filter(is_staff=True)
            admin_found = None
            
            for admin in admin_users:
                # Buscar por email coincidente o por relación con el instituto
                if admin.email == instituto.email_contacto:
                    admin_found = admin
                    break
            
            if admin_found:
                return Response({
                    'admin_found': True,
                    'username': admin_found.username,
                    'first_name': admin_found.first_name,
                    'last_name': admin_found.last_name,
                    'email': admin_found.email,
                    'is_staff': admin_found.is_staff,
                    'is_active': admin_found.is_active,
                    'date_joined': admin_found.date_joined
                })
            else:
                return Response({
                    'admin_found': False,
                    'message': 'No se encontró administrador para este instituto'
                })
                
        except Exception as e:
            return Response({
                'error': f'Error al buscar administrador: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

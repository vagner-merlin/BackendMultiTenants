"""
Django settings for mysite project con django-tenants
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&q-+f&e6ilh9e$@80ugnj-6u6k#(kp(0v!chggm)0^-w16j8&d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']  # Permitir todos los hosts para desarrollo

# ============================================
# CONFIGURACIÓN DE DJANGO-TENANTS
# ============================================

# Apps que se comparten entre TODOS los tenants (esquema público)
SHARED_APPS = [
    'django_tenants',  # OBLIGATORIO y debe ir primero
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',  # Para tokens de autenticación
    
    # TUS APPS COMPARTIDAS (para gestión de institutos)
    'app_shared_Manager',  # Corregido - solo esta app existe
]

# Apps que son específicas de cada tenant (cada instituto)
TENANT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth', 
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',  # Para tokens de autenticación
    
    # TUS APPS DE TENANT (específicas por instituto)
    'app_tenant_User',  # Nueva app para usuarios
]

# TODAS las apps juntas (django-tenants las maneja automáticamente)
INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

# Modelos principales de django-tenants
TENANT_MODEL = "app_shared_Manager.Instituto"
TENANT_DOMAIN_MODEL = "app_shared_Manager.Domain"

# ============================================
# MIDDLEWARE - ORDEN IMPORTANTE
# ============================================
MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'
PUBLIC_SCHEMA_URLCONF = 'mysite.urls_public'  # URLs para esquema público
TENANT_SCHEMA_URLCONF = 'mysite.urls_tenant'   # URLs para cada tenant

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

# ============================================
# BASE DE DATOS - POSTGRESQL OBLIGATORIO
# ============================================
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',  # Motor específico de django-tenants
        'NAME': 'postgres',
        'USER': 'postgres', 
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': 5433,
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# ============================================
# REST FRAMEWORK CON AUTENTICACIÓN POR TOKEN
# ============================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Cambiar a requerir autenticación
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ],
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'

# Configuración para archivos de medios (fotos)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

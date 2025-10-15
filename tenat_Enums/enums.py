# Enumeraciones para el sistema financiero multi-tenant

# Enumeraciones para tipos de plan
ENUM_PLAN_CHOICES = [
    ('gratis', 'Gratis'),
    ('basico', 'Básico'),
    ('profesional', 'Profesional'),
]

# Enumeraciones para estado SaaS
ENUM_ESTADO_SAAS_CHOICES = [
    ('en_prueba', 'En Prueba'),
    ('activo', 'Activo'),
    ('cancelado', 'Cancelado'),
]

# Enumeraciones para temas de interfaz
ENUM_TEMA_CHOICES = [
    ('automatico', 'Automático'),
    ('oscuro', 'Oscuro'),
    ('claro', 'Claro'),
]

# Enumeraciones para estado de crédito
ENUM_ESTADO_CREDITO_CHOICES = [
    ('pendiente', 'Pendiente'),
    ('analisis', 'En Análisis'),
    ('aprobado', 'Aprobado'),
    ('rechazado', 'Rechazado'),
    ('activo', 'Activo'),
    ('finalizado', 'Finalizado'),
]

# Enumeraciones para licencias on-premise
LICENCIA_ON_PREMISE_CHOICES = [
    ('razon_social', 'Razón Social'),
    ('email_contacto', 'Email de Contacto'),
    ('version', 'Versión'),
    ('fecha_compra', 'Fecha de Compra'),
    ('fecha_sin_soporte', 'Fecha Sin Soporte'),
]

# Valores por defecto
DEFAULT_PLAN = 'gratis'
DEFAULT_ESTADO_SAAS = 'en_prueba'
DEFAULT_TEMA = 'automatico'
DEFAULT_ESTADO_CREDITO = 'pendiente'
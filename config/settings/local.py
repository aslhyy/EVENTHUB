from .base import *

DEBUG = True
SECRET_KEY = "dev-secret-key"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]
APPEND_SLASH = False

# 🔥 FORZAR configuración sin autenticación
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
    'UNAUTHENTICATED_USER': None,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    "TITLE": "EventHub API",
    "DESCRIPTION": "EventHub backend",
    "VERSION": "1.0.0",
    "SERVE_PERMISSIONS": [],
    "SERVE_PUBLIC": True,
}

# Quitar CSRF middleware
MIDDLEWARE = [m for m in MIDDLEWARE if 'csrf' not in m.lower()]
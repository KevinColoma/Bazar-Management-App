"""
WSGI config for BAZAR_APP project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BAZAR_APP.settings')

application = get_wsgi_application()

# Crear superusuario automáticamente al iniciar la aplicación
try:
    from django.core.management import call_command
    print("🚀 Intentando crear superusuario automáticamente...")
    call_command('create_superuser_auto')
    print("✅ Proceso de superusuario completado")
except Exception as e:
    print(f"⚠️ Error en creación automática de superusuario: {e}")

# Para Vercel
app = application

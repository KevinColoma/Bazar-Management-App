#!/usr/bin/env python
"""
Script para crear superusuario automáticamente durante el despliegue
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BAZAR_APP.settings')
django.setup()

from django.contrib.auth import get_user_model
from App_Login.models import Profile

User = get_user_model()

def create_superuser():
    email = os.environ.get('SUPERUSER_EMAIL', 'admin@bazar.com')
    password = os.environ.get('SUPERUSER_PASSWORD', 'admin123')
    
    if not User.objects.filter(email=email).exists():
        print(f'Creando superusuario con email: {email}')
        user = User.objects.create_superuser(
            email=email,
            password=password
        )
        
        # Actualizar el perfil asociado (se crea automáticamente por el signal)
        if hasattr(user, 'profile'):
            profile = user.profile
            profile.username = 'admin'
            profile.full_name = 'Administrador del Sistema'
            profile.save()
        
        print('✅ Superusuario creado exitosamente!')
        print(f'📧 Email: {email}')
        print(f'🔑 Password: {password}')
        print('🔗 Panel admin: /admin/')
    else:
        print('ℹ️  Superusuario ya existe')

if __name__ == '__main__':
    create_superuser()

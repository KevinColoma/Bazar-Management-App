import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from App_Login.models import Profile

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser automatically'

    def handle(self, *args, **options):
        email = os.environ.get('SUPERUSER_EMAIL', 'admin@bazar.com')
        password = os.environ.get('SUPERUSER_PASSWORD', 'admin123')
        
        # Eliminar usuario existente si existe (para asegurar recreación)
        if User.objects.filter(email=email).exists():
            self.stdout.write(f'🗑️  Eliminando superusuario existente: {email}')
            User.objects.filter(email=email).delete()
        
        self.stdout.write(f'👤 Creando superusuario con email: {email}')
        user = User.objects.create_superuser(
            email=email,
            password=password
        )
        
        # Actualizar el perfil asociado (se crea automáticamente por el signal)
        try:
            if hasattr(user, 'profile'):
                profile = user.profile
                profile.username = 'admin'
                profile.full_name = 'Administrador del Sistema'
                profile.save()
                self.stdout.write('👤 Perfil actualizado')
        except Exception as e:
            self.stdout.write(f'⚠️  Advertencia en perfil: {e}')
        
        self.stdout.write(
            self.style.SUCCESS('✅ Superusuario creado exitosamente!')
        )
        self.stdout.write(f'📧 Email: {email}')
        self.stdout.write(f'🔑 Password: {password}')
        self.stdout.write('🔗 Panel admin: /admin/')
        self.stdout.write('=' * 50)

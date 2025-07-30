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
        
        if not User.objects.filter(email=email).exists():
            self.stdout.write(f'Creando superusuario con email: {email}')
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
            
            self.stdout.write(
                self.style.SUCCESS('✅ Superusuario creado exitosamente!')
            )
            self.stdout.write(f'📧 Email: {email}')
            self.stdout.write(f'🔑 Password: {password}')
            self.stdout.write('🔗 Panel admin: /admin/')
        else:
            self.stdout.write(
                self.style.WARNING('ℹ️  Superusuario ya existe')
            )

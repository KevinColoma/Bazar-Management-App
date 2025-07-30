#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🔧 Instalando dependencias..."
pip install -r requirements.txt

echo "📦 Recopilando archivos estáticos..."
python manage.py collectstatic --no-input

echo "🗄️  Ejecutando migraciones..."
python manage.py migrate

echo "👤 Creando superusuario automáticamente..."
python manage.py create_superuser_auto || echo "❌ Error creando superusuario"

echo "✅ Build completado exitosamente!"
echo "🔑 Credenciales: admin@bazar.com / admin123"

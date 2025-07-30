#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🔧 Instalando dependencias..."
pip install -r requirements.txt

echo "📦 Recopilando archivos estáticos..."
python manage.py collectstatic --no-input

echo "🗄️  Ejecutando migraciones..."
python manage.py migrate

echo "👤 Creando superusuario..."
python manage.py create_superuser_auto

echo "✅ Build completado exitosamente!"

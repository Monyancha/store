#!/bin/bash

# Railway deployment script for Cynthia Online Store

echo "🚀 Starting Railway deployment for Cynthia Online Store..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "👤 Setting up admin user..."
python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'cynthy8samuels@gmail.com', 'admin')
    print('✅ Admin user created')
else:
    print('ℹ️ Admin user already exists')
"

# Setup demo data (only if in development or if environment variable is set)
if [ "$SETUP_DEMO_DATA" = "true" ]; then
    echo "🌱 Setting up demo data..."
    python scripts/setup_demo_data.py
else
    echo "ℹ️ Skipping demo data setup (set SETUP_DEMO_DATA=true to enable)"
fi

echo "✅ Railway deployment setup complete!"
echo "🔗 Contact: cynthy8samuels@gmail.com | Phone: +254798534856"

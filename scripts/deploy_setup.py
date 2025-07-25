#!/usr/bin/env python
"""
Deployment setup script for Cynthia Online Store
Handles migrations and initial setup for production deployment
"""
import os
import sys
import django
from django.core.management import execute_from_command_line
from django.db import connection

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def check_database_connection():
    """Check if database is accessible"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def run_migrations():
    """Run Django migrations"""
    try:
        print("🔄 Running migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        print("✅ Migrations completed successfully")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def collect_static():
    """Collect static files"""
    try:
        print("🔄 Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✅ Static files collected successfully")
        return True
    except Exception as e:
        print(f"❌ Static files collection failed: {e}")
        return False

def create_superuser_if_needed():
    """Create superuser if it doesn't exist"""
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(is_superuser=True).exists():
            print("🔄 Creating superuser...")
            User.objects.create_superuser(
                username='admin',
                email='cynthy8samuels@gmail.com',
                password='admin'
            )
            print("✅ Superuser created successfully")
        else:
            print("ℹ️  Superuser already exists")
        return True
    except Exception as e:
        print(f"❌ Superuser creation failed: {e}")
        return False

def main():
    """Main deployment setup function"""
    print("🚀 Starting Cynthia Online Store deployment setup...")
    print("="*60)
    
    steps = [
        ("Database Connection", check_database_connection),
        ("Migrations", run_migrations),
        ("Static Files", collect_static),
        ("Superuser", create_superuser_if_needed),
    ]
    
    failed_steps = []
    
    for step_name, step_function in steps:
        print(f"\n📋 {step_name}...")
        if not step_function():
            failed_steps.append(step_name)
    
    print("\n" + "="*60)
    if failed_steps:
        print(f"❌ Deployment setup completed with errors in: {', '.join(failed_steps)}")
        return 1
    else:
        print("✅ Deployment setup completed successfully!")
        print("🌟 Cynthia Online Store is ready for production!")
        print("📧 Contact: cynthy8samuels@gmail.com")
        print("📞 Phone: +254798534856")
        return 0

if __name__ == '__main__':
    sys.exit(main())

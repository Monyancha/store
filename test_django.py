#!/usr/bin/env python3
import sys
import os

print("Python path:", sys.executable)
print("Python version:", sys.version)
print("Current directory:", os.getcwd())

try:
    import django
    print("Django version:", django.get_version())
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    print("Django setup successful")
    
    from django.contrib.auth.models import User
    print("User model imported successfully")
    print("Number of users:", User.objects.count())
    
except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()

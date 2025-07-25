# 🚂 Railway Deployment Troubleshooting Guide

## Common Railway Deployment Issues & Solutions

### 1. **Port Error: '$PORT' is not a valid port number**

#### Problem
```
Error: '$PORT' is not a valid port number.
```

#### Solutions

**Option A: Fixed Procfile (Recommended)**
```bash
# Create correct Procfile
echo "web: gunicorn config.wsgi:application --bind 0.0.0.0:\$PORT" > Procfile
```

**Option B: Alternative Procfile formats**
```bash
# Method 1: With fallback port
echo "web: gunicorn config.wsgi:application --bind 0.0.0.0:\${PORT:-8000}" > Procfile

# Method 2: Let Railway handle binding
echo "web: gunicorn config.wsgi:application" > Procfile

# Method 3: Using python manage.py runserver (not recommended for production)
echo "web: python manage.py runserver 0.0.0.0:\$PORT" > Procfile
```

**Option C: Use nixpacks.toml instead**
```toml
# nixpacks.toml
[start]
cmd = 'gunicorn config.wsgi:application --bind 0.0.0.0:$PORT'
```

### 2. **Database Connection Issues**

#### Problem
```
django.core.exceptions.ImproperlyConfigured: settings.DATABASES is improperly configured
```

#### Solution
```python
# In settings.py
import dj_database_url

if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    # Fallback to SQLite for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

### 3. **Static Files Not Loading**

#### Problem
CSS/JS files not loading in production.

#### Solution
```python
# In settings.py
import os

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Add to Procfile or build phase
# python manage.py collectstatic --noinput
```

### 4. **CORS Issues on Railway**

#### Problem
```
Access to XMLHttpRequest at 'https://your-app.up.railway.app/api/...' from origin 'https://frontend.com' has been blocked by CORS policy
```

#### Solution
```python
# In settings.py
CORS_ALLOWED_ORIGINS = [
    "https://your-app.up.railway.app",
    "https://*.up.railway.app",
    "https://your-frontend-domain.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://your-app.up.railway.app",
    "https://*.up.railway.app",
]
```

### 5. **Environment Variables Not Working**

#### Problem
Environment variables not being read correctly.

#### Solution
```bash
# Set in Railway dashboard under Variables tab:
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://... (Railway provides this automatically)
ALLOWED_HOSTS=your-app.up.railway.app
```

### 6. **Migration Issues**

#### Problem
```
django.db.utils.ProgrammingError: relation "app_model" does not exist
```

#### Solution
```bash
# Add to your deployment script or Railway build phase
python manage.py migrate --noinput
```

#### Or use a release command in nixpacks.toml:
```toml
[phases.setup]
nixPkgs = ['python310', 'postgresql']

[phases.install] 
cmds = ['pip install -r requirements.txt']

[phases.build]
cmds = [
    'python manage.py collectstatic --noinput',
    'python manage.py migrate --noinput'
]
```

### 7. **Memory/Timeout Issues**

#### Problem
```
Error: Process crashed with exit code 137 (out of memory)
```

#### Solutions

**Option A: Optimize gunicorn settings**
```bash
# In Procfile
web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 60 --max-requests 1000
```

**Option B: Add memory limit handling**
```python
# In settings.py
import os

# Reduce memory usage
if 'RAILWAY_ENVIRONMENT' in os.environ:
    DEBUG = False
    # Disable debug toolbar and other debug tools
    INSTALLED_APPS = [app for app in INSTALLED_APPS if 'debug' not in app.lower()]
```

### 8. **SSL/HTTPS Issues**

#### Problem
Mixed content errors or SSL certificate issues.

#### Solution
```python
# In settings.py
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

## Quick Railway Deployment Checklist

### ✅ Pre-deployment Checklist
- [ ] Procfile exists with correct syntax
- [ ] requirements.txt is up to date
- [ ] DATABASE_URL handling in settings.py
- [ ] Static files configuration
- [ ] Environment variables set in Railway
- [ ] CORS configuration for your domain
- [ ] Debug=False for production

### ✅ Required Files for Railway
```
your-project/
├── Procfile                 # Web server command
├── requirements.txt         # Python dependencies  
├── manage.py               # Django management
├── config/
│   ├── settings.py         # Django settings
│   └── wsgi.py            # WSGI application
└── apps/                   # Your Django apps
```

### ✅ Essential Environment Variables
```bash
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://... (auto-provided by Railway)
ALLOWED_HOSTS=your-app.up.railway.app
```

### ✅ Working Procfile Examples

**Basic Gunicorn (Recommended)**
```
web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

**Gunicorn with optimization**
```
web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 60
```

**Django runserver (Development only)**
```
web: python manage.py runserver 0.0.0.0:$PORT
```

## Getting Help

### Railway Logs
```bash
# View logs in Railway dashboard or CLI
railway logs
```

### Django Debug
```python
# Temporarily enable debug for troubleshooting
DEBUG = True
ALLOWED_HOSTS = ['*']  # Temporarily allow all hosts
```

### Test Locally First
```bash
# Test with production-like settings locally
export DEBUG=False
export DATABASE_URL=sqlite:///db.sqlite3
python manage.py runserver
```

## 🚀 Quick Fix Command

Run this script to fix common Railway deployment issues:

```bash
# Run the Railway deployment script
./scripts/deploy_railway.sh
```

This will:
1. Create proper Procfile
2. Update requirements.txt  
3. Create Railway configuration files
4. Provide deployment instructions

---

**Need more help?** 
- Railway Docs: https://docs.railway.app/
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
- Contact: cynthy8samuels@gmail.com

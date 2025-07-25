#!/bin/bash
# Railway Deployment Script
# This script helps prepare and deploy the Cynthia Online Store to Railway

echo "🚀 Preparing Cynthia Online Store for Railway Deployment..."

# 1. Create/Update Procfile
echo "📝 Creating Procfile..."
cat > Procfile << 'EOF'
web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
EOF

# 2. Update requirements.txt
echo "📦 Updating requirements.txt..."
pip freeze > requirements.txt

# 3. Create railway.json for configuration
echo "⚙️ Creating railway.json..."
cat > railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "nixpacks"
  },
  "deploy": {
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF

# 4. Create nixpacks.toml for build configuration
echo "🔧 Creating nixpacks.toml..."
cat > nixpacks.toml << 'EOF'
[phases.setup]
nixPkgs = ['python310', 'postgresql']

[phases.install]
cmds = ['pip install -r requirements.txt']

[phases.build]
cmds = ['python manage.py collectstatic --noinput']

[start]
cmd = 'gunicorn config.wsgi:application --bind 0.0.0.0:$PORT'
EOF

echo "✅ Deployment files created successfully!"
echo ""
echo "📋 Next Steps for Railway Deployment:"
echo "1. Push your code to GitHub"
echo "2. Connect your GitHub repository to Railway"
echo "3. Set the following environment variables in Railway:"
echo "   - SECRET_KEY=your-secret-key"
echo "   - DEBUG=False"
echo "   - DATABASE_URL=postgresql://... (Railway will provide this)"
echo "   - ALLOWED_HOSTS=your-app-name.up.railway.app"
echo ""
echo "4. Deploy and your app will be available at:"
echo "   https://your-app-name.up.railway.app"
echo ""
echo "🔗 Important URLs after deployment:"
echo "   - API: https://your-app-name.up.railway.app/api/"
echo "   - Swagger: https://your-app-name.up.railway.app/swagger/"
echo "   - Admin: https://your-app-name.up.railway.app/admin/"
echo ""
echo "🎉 Ready for Railway deployment!"

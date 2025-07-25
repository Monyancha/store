from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection
from django.core.cache import cache
from django.conf import settings
import redis

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Comprehensive health check endpoint"""
    health_status = {
        'status': 'healthy',
        'service': 'Cynthia Online Store API',
        'version': '1.0.0',
        'timestamp': request.META.get('HTTP_DATE'),
        'checks': {}
    }
    
    # Database check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_status['checks']['database'] = 'healthy'
    except Exception as e:
        health_status['checks']['database'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    # Cache check
    try:
        cache.set('health_check', 'test', 10)
        cache.get('health_check')
        health_status['checks']['cache'] = 'healthy'
    except Exception as e:
        health_status['checks']['cache'] = f'unhealthy: {str(e)}'
    
    # Redis check (if configured)
    if hasattr(settings, 'REDIS_URL'):
        try:
            r = redis.from_url(settings.REDIS_URL)
            r.ping()
            health_status['checks']['redis'] = 'healthy'
        except Exception as e:
            health_status['checks']['redis'] = f'unhealthy: {str(e)}'
    
    return Response(health_status)

@api_view(['GET'])
@permission_classes([AllowAny])
def system_info(request):
    """System information endpoint"""
    return Response({
        'service': 'Cynthia Online Store API',
        'version': '1.0.0',
        'contact': {
            'email': 'cynthy8samuels@gmail.com',
            'phone': '+254798534856'
        },
        'business': {
            'name': 'Cynthia Online Store',
            'location': 'Nairobi, Kenya'
        }
    })

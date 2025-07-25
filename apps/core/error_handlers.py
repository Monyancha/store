from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

def handler404(request, exception):
    """Custom 404 error handler"""
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Not Found',
            'message': 'The requested API endpoint was not found.',
            'status_code': 404,
            'contact': 'cynthy8samuels@gmail.com'
        }, status=404)
    
    return render(request, '404.html', status=404)

def handler403(request, exception):
    """Custom 403 error handler"""
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource.',
            'status_code': 403,
            'contact': 'cynthy8samuels@gmail.com'
        }, status=403)
    
    return render(request, '403.html', status=403)

def handler500(request):
    """Custom 500 error handler"""
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Internal Server Error',
            'message': 'Something went wrong on our end. Please try again later.',
            'status_code': 500,
            'contact': 'cynthy8samuels@gmail.com'
        }, status=500)
    
    return render(request, '500.html', status=500)

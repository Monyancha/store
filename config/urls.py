from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger/OpenAPI schema configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Cynthia Online Store API",
        default_version='v1',
        description="""
        # Cynthia Online Store Backend API
        
        A comprehensive e-commerce backend service built with Django REST Framework.
        
        ## About Cynthia Online Store
        Your one-stop shop for quality products with excellent customer service.
        
        **Contact Information:**
        - Email: cynthy8samuels@gmail.com
        - Phone: +254798534856
        - Location: Nairobi, Kenya
        
        ## Features
        - User authentication and authorization (OAuth2/OpenID Connect)
        - Customer management with detailed profiles
        - Hierarchical product categories (unlimited depth)
        - Product management with inventory tracking
        - Order processing with SMS and email notifications
        - Analytics and reporting
        - RESTful API with comprehensive documentation
        
        ## Authentication
        This API supports multiple authentication methods:
        - **Token Authentication**: Use `Authorization: Token <your-token>` header
        - **Session Authentication**: Login through the browsable API
        - **OAuth2/OpenID Connect**: For third-party integrations
        
        **Default Admin Credentials:**
        - Username: admin
        - Password: admin
        
        ## Testing
        You can test the API using:
        - This Swagger UI interface
        - Postman collection (available in the repository)
        - cURL commands
        - Python requests library
        
        ## Support
        For support, please contact: cynthy8samuels@gmail.com
        """,
        terms_of_service="https://cynthia-online-store.com/terms/",
        contact=openapi.Contact(email="cynthy8samuels@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)

# API Router
router = DefaultRouter()

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Root redirect to API documentation
    path('', RedirectView.as_view(url='/swagger/', permanent=False), name='index'),
    
    # Health check
    path('health/', include('apps.core.urls')),
    
    # Django authentication URLs (for Swagger login)
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    
    # API endpoints
    path('api/', include(router.urls)),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/customers/', include('apps.customers.urls')),
    path('api/categories/', include('apps.categories.urls')),
    path('api/products/', include('apps.products.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/inventory/', include('apps.inventory.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    
    # Authentication
    path('oidc/', include('mozilla_django_oidc.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # API Documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom admin configuration
admin.site.site_header = "Cynthia Online Store Administration"
admin.site.site_title = "Cynthia Online Store Admin"
admin.site.index_title = "Welcome to Cynthia Online Store Administration"

# Custom error handlers
handler404 = 'apps.core.error_handlers.handler404'
handler403 = 'apps.core.error_handlers.handler403'
handler500 = 'apps.core.error_handlers.handler500'

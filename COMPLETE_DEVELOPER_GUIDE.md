# 🛍️ Cynthia Online Store - Complete Developer Documentation

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Features & Implementation](#features--implementation)
4. [Setup & Installation](#setup--installation)
5. [API Documentation](#api-documentation)
6. [Best Practices Applied](#best-practices-applied)
7. [Challenges & Solutions](#challenges--solutions)
8. [Interview Questions & Answers](#interview-questions--answers)
9. [Performance & Optimization](#performance--optimization)
10. [Security Implementation](#security-implementation)
11. [Testing Strategy](#testing-strategy)
12. [Deployment Guide](#deployment-guide)

---

## 📊 Project Overview

### Business Context
**Cynthia Online Store** is a comprehensive e-commerce backend service built for **Savannah Informatics Backend Role Assessment**. It demonstrates enterprise-level Django REST API development with advanced features like hierarchical categories, inventory management, order processing, and customer relationship management.

### Tech Stack
- **Backend**: Django 5.2.1, Django REST Framework 3.16.0
- **Database**: PostgreSQL (Production), SQLite (Development), MySQL (Optional)
- **Authentication**: Token-based, Session-based, OAuth2/OpenID Connect
- **Documentation**: drf-yasg (Swagger/OpenAPI)
- **Caching**: Redis (Production), LocMem (Development)
- **SMS Integration**: Africa's Talking API
- **Deployment**: Docker, Vercel-compatible, Heroku

### Key Business Metrics
- **Contact**: cynthy8samuels@gmail.com
- **Phone**: +254798534856
- **Location**: Nairobi, Kenya

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Django REST    │    │   Database      │
│   (Any Client)  │◄──►│   API Server     │◄──►│   PostgreSQL    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                       ┌────────┼────────┐
                       │        │        │
              ┌─────────▼───┐ ┌──▼──┐ ┌───▼────┐
              │   Redis     │ │SMS  │ │ Email  │
              │   Cache     │ │API  │ │Service │
              └─────────────┘ └─────┘ └────────┘
```

### Django App Structure

```
cynthia-online-store/
├── config/                 # Project settings
├── apps/
│   ├── authentication/     # User management & auth
│   ├── customers/          # Customer profiles & addresses
│   ├── categories/         # Hierarchical product categories
│   ├── products/           # Product catalog & inventory
│   ├── orders/             # Order processing & fulfillment
│   ├── inventory/          # Stock management & alerts
│   ├── analytics/          # Business intelligence
│   └── core/               # Shared utilities & middleware
├── templates/              # Custom error pages & auth
├── static/                 # Static files
├── media/                  # User uploads
└── scripts/               # Setup & deployment scripts
```

---

## 🚀 Features & Implementation

### 1. **Authentication System** 🔐

#### Implementation Details
```python
# Multiple authentication backends
AUTHENTICATION_BACKENDS = [
    'mozilla_django_oidc.auth.OIDCAuthenticationBackend',  # OAuth2/OpenID
    'django.contrib.auth.backends.ModelBackend',          # Standard Django
]

# Token-based authentication for APIs
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'mozilla_django_oidc.contrib.drf.OIDCAuthentication',
    ],
}
```

#### Features
- **User Registration**: Email verification, password validation
- **Login/Logout**: Session and token-based authentication
- **Password Management**: Change password, reset via email
- **Profile Management**: User profile updates and preferences
- **OAuth2/OpenID Connect**: Third-party authentication support

#### API Endpoints
```bash
POST /api/auth/register/        # User registration
POST /api/auth/login/           # User login
POST /api/auth/logout/          # User logout
GET  /api/auth/profile/         # Get user profile
PUT  /api/auth/profile/         # Update user profile
POST /api/auth/change-password/ # Change password
```

### 2. **Customer Management System** 👥

#### Advanced Customer Model
```python
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_type = models.CharField(choices=CUSTOMER_TYPES)
    id_number = models.CharField(unique=True)
    phone_number = models.CharField()
    date_of_birth = models.DateField()
    gender = models.CharField(choices=GENDER_CHOICES)
    loyalty_points = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(max_digits=12, decimal_places=2)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2)
    is_verified = models.BooleanField(default=False)
```

#### Features
- **Customer Types**: Individual, Premium, Business classifications
- **Address Management**: Multiple addresses per customer
- **Financial Tracking**: Credit limits, total spent, payment history
- **Loyalty System**: Points accumulation and redemption
- **Business Customers**: Extended features for B2B operations

### 3. **Hierarchical Category System** 🏷️

#### Unlimited Depth Categories
```python
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True)
    level = models.PositiveIntegerField(default=0)
    path = models.CharField(max_length=255)  # Materialized path
    
    def save(self, *args, **kwargs):
        # Auto-calculate level and path
        if self.parent:
            self.level = self.parent.level + 1
            self.path = f"{self.parent.path}/{self.pk}"
        else:
            self.level = 0
            self.path = str(self.pk)
        super().save(*args, **kwargs)
```

#### Features
- **Unlimited Hierarchy**: Any depth category nesting
- **Category Attributes**: Dynamic attributes per category
- **SEO Optimization**: Slugs, meta descriptions, structured data
- **Business Rules**: Category-specific pricing and shipping rules

### 4. **Advanced Product Management** 📦

#### Product Variants & Types
```python
class Product(models.Model):
    PRODUCT_TYPES = (
        ('simple', 'Simple Product'),
        ('variable', 'Variable Product'),
        ('grouped', 'Grouped Product'),
        ('digital', 'Digital Product'),
    )
    
    product_type = models.CharField(choices=PRODUCT_TYPES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL)
    variants = models.ManyToManyField('ProductVariant')
```

#### Features
- **Product Types**: Simple, Variable, Grouped, Digital products
- **Inventory Tracking**: Real-time stock levels, low-stock alerts
- **Product Variants**: Size, color, material variations
- **Image Gallery**: Multiple product images with optimization
- **Reviews & Ratings**: Customer feedback system
- **SEO Features**: Meta tags, structured data, sitemap integration

### 5. **Order Processing System** 🛒

#### Order State Management
```python
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    )
    
    def transition_to(self, new_status):
        # State machine implementation
        valid_transitions = self.get_valid_transitions()
        if new_status in valid_transitions:
            self.status = new_status
            self.save()
            self.send_status_notification()
```

#### Features
- **Order State Machine**: Controlled status transitions
- **Payment Integration**: Multiple payment gateway support
- **Shipping Management**: Multiple shipping options and tracking
- **Notifications**: SMS and email notifications via Africa's Talking
- **Invoice Generation**: PDF invoices and receipts

### 6. **Inventory Management** 📊

#### Real-time Stock Tracking
```python
class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = (
        ('purchase', 'Stock Purchase'),
        ('sale', 'Sale'),
        ('adjustment', 'Stock Adjustment'),
        ('return', 'Return'),
        ('damage', 'Damage/Loss'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    transaction_type = models.CharField(choices=TRANSACTION_TYPES)
    quantity = models.IntegerField()
    reference_number = models.CharField(unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
```

#### Features
- **Transaction Logging**: Every stock movement tracked
- **Automated Alerts**: Low stock notifications
- **Stock Adjustments**: Manual inventory corrections
- **Reporting**: Stock movement reports and analytics

### 7. **Analytics & Reporting** 📈

#### Business Intelligence
```python
class SalesReport(models.Model):
    date = models.DateField()
    total_sales = models.DecimalField(max_digits=15, decimal_places=2)
    total_orders = models.PositiveIntegerField()
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2)
    top_selling_products = models.JSONField()
    customer_segments = models.JSONField()
```

#### Features
- **Sales Analytics**: Revenue tracking, trend analysis
- **Customer Analytics**: Behavior patterns, segmentation
- **Product Analytics**: Performance metrics, popularity trends
- **Real-time Dashboards**: Live business metrics

---

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.11+ 
- PostgreSQL 12+ (for production)
- Redis 6+ (for caching)
- Git

### Quick Setup

#### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
# Clone repository
git clone <repository-url>
cd cynthia-online-store

# Run automated setup
setup_windows.bat
```

**Ubuntu/Linux:**
```bash
# Clone repository
git clone <repository-url>
cd cynthia-online-store

# Make script executable and run
chmod +x setup_ubuntu.sh
./setup_ubuntu.sh
```

#### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# Ubuntu/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Environment configuration
cp .env.example .env
# Edit .env with your database credentials

# 5. Database setup
python manage.py migrate

# 6. Create superuser
python scripts/deploy_setup.py

# 7. Load demo data (optional)
python scripts/setup_demo_data.py

# 8. Collect static files
python manage.py collectstatic --noinput

# 9. Start development server
python manage.py runserver
```

### Environment Variables

```bash
# Database Configuration
DATABASE_ENGINE=postgresql  # postgresql, mysql, sqlite3
DB_NAME=cynthia-store
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# Security
SECRET_KEY=your-secret-key
DEBUG=True  # Set to False in production
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# SMS Configuration (Africa's Talking)
AFRICASTALKING_USERNAME=your_username
AFRICASTALKING_API_KEY=your_api_key
AFRICASTALKING_SENDER=YourSender

# Cache Configuration
REDIS_URL=redis://localhost:6379/1

# OAuth2/OpenID Connect (Optional)
OIDC_RP_CLIENT_ID=your_client_id
OIDC_RP_CLIENT_SECRET=your_client_secret
```

---

## 📚 API Documentation

### Base URL
- **Local**: `http://localhost:8000/api/`
- **Production**: `https://your-app.herokuapp.com/api/` or `https://your-app.vercel.app/api/`

### Authentication

#### Token Authentication
```bash
# Get token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'

# Use token in requests
curl -H "Authorization: Token your-token-here" \
  http://localhost:8000/api/products/
```

#### Session Authentication (Swagger UI)
1. Visit `/swagger/`
2. Click "Login" in top-right corner
3. Enter credentials: admin/admin
4. Try API endpoints directly in Swagger

### Core API Endpoints

#### Categories API
```bash
GET    /api/categories/                 # List all categories
POST   /api/categories/                 # Create category
GET    /api/categories/{id}/            # Get category details
PUT    /api/categories/{id}/            # Update category
DELETE /api/categories/{id}/            # Delete category
GET    /api/categories/{id}/children/   # Get child categories
```

#### Products API
```bash
GET    /api/products/                   # List products (with filters)
POST   /api/products/                   # Create product
GET    /api/products/{id}/              # Get product details
PUT    /api/products/{id}/              # Update product
DELETE /api/products/{id}/              # Delete product
GET    /api/products/{id}/reviews/      # Get product reviews
POST   /api/products/{id}/reviews/      # Add product review
```

#### Orders API
```bash
GET    /api/orders/                     # List user orders
POST   /api/orders/                     # Create order
GET    /api/orders/{id}/                # Get order details
PUT    /api/orders/{id}/status/         # Update order status
GET    /api/orders/{id}/items/          # Get order items
```

#### Customers API
```bash
GET    /api/customers/                  # List customers (admin only)
POST   /api/customers/                  # Create customer
GET    /api/customers/{id}/             # Get customer details
PUT    /api/customers/{id}/             # Update customer
GET    /api/customers/{id}/addresses/   # Get customer addresses
POST   /api/customers/{id}/addresses/   # Add customer address
```

### Filtering & Search

```bash
# Filter products by category
GET /api/products/?category=electronics

# Search products
GET /api/products/?search=laptop

# Filter by price range
GET /api/products/?min_price=100&max_price=1000

# Sort products
GET /api/products/?ordering=-created_at

# Pagination
GET /api/products/?page=2&page_size=20
```

---

## 🎯 Best Practices Applied

### 1. **Code Organization**

#### Django Apps Structure
```python
# Single responsibility principle
apps/
├── authentication/  # Only handles user auth
├── customers/       # Only handles customer data
├── products/        # Only handles product catalog
├── orders/          # Only handles order processing
└── core/           # Shared utilities
```

#### Model Design
```python
class BaseModel(models.Model):
    """Abstract base model with common fields"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Product(BaseModel):
    """Inherits common fields and behavior"""
    name = models.CharField(max_length=200)
    # ... other fields
```

### 2. **API Design**

#### RESTful Conventions
```python
# Clear, consistent URL patterns
urlpatterns = [
    path('products/', ProductListCreateView.as_view()),           # GET, POST
    path('products/<uuid:pk>/', ProductDetailView.as_view()),    # GET, PUT, DELETE
    path('products/<uuid:pk>/reviews/', ReviewListView.as_view()), # Nested resources
]
```

#### Serializer Best Practices
```python
class ProductSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='category', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category', 'category_details']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be positive")
        return value
```

### 3. **Security Implementation**

#### Input Validation
```python
# Custom validators
def validate_phone_number(value):
    if not re.match(r'^\+254[0-9]{9}$', value):
        raise ValidationError('Invalid Kenyan phone number format')

# Model-level validation
class Customer(models.Model):
    phone_number = models.CharField(validators=[validate_phone_number])
```

#### Permission Classes
```python
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only to owner
        return obj.owner == request.user
```

### 4. **Database Optimization**

#### Query Optimization
```python
# Use select_related for foreign keys
products = Product.objects.select_related('category', 'brand').all()

# Use prefetch_related for many-to-many
products = Product.objects.prefetch_related('variants', 'images').all()

# Custom queryset managers
class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)
    
    def in_stock(self):
        return self.filter(stock_quantity__gt=0)

class Product(models.Model):
    objects = ProductQuerySet.as_manager()
```

#### Database Indexing
```python
class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    sku = models.CharField(max_length=50, unique=True, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['created_at']),
        ]
```

### 5. **Error Handling**

#### Custom Exception Handler
```python
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'error': True,
            'message': response.data.get('detail', 'An error occurred'),
            'status_code': response.status_code,
            'timestamp': timezone.now().isoformat(),
            'contact': 'cynthy8samuels@gmail.com'
        }
        response.data = custom_response_data
    
    return response
```

### 6. **Testing Strategy**

#### Comprehensive Test Coverage
```python
class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Electronics')
    
    def test_create_product(self):
        data = {
            'name': 'Test Product',
            'price': '99.99',
            'category': self.category.id
        }
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 1)
```

---

## 🔧 Challenges & Solutions

### 1. **Category Hierarchy Management**

#### Challenge
Creating unlimited depth categories while maintaining performance and avoiding N+1 queries.

#### Solution
```python
# Materialized Path Pattern
class Category(models.Model):
    path = models.CharField(max_length=255)  # e.g., "1/3/7"
    level = models.PositiveIntegerField(default=0)
    
    def get_ancestors(self):
        # Get all ancestors in single query
        if not self.path:
            return Category.objects.none()
        
        ancestor_ids = self.path.split('/')[:-1]
        return Category.objects.filter(id__in=ancestor_ids)
    
    def get_descendants(self):
        # Get all descendants in single query
        return Category.objects.filter(
            path__startswith=f"{self.path}/",
            level__gt=self.level
        )
```

### 2. **Database Setup Duplication Issues**

#### Challenge
Demo data setup failing due to unique constraint violations when run multiple times.

#### Solution
```python
# Use get_or_create instead of create
def create_categories(self):
    for category_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=category_data['name'],
            defaults={
                'description': category_data['description'],
                'parent': category_data.get('parent')
            }
        )
        if created:
            print(f'✅ Category created: {category.name}')
        else:
            print(f'ℹ️  Category already exists: {category.name}')
```

### 3. **CORS Configuration for Multiple Deployments**

#### Challenge
Supporting multiple deployment platforms (Vercel, Heroku, local development) with proper CORS.

#### Solution
```python
# Dynamic CORS configuration
CORS_ALLOWED_ORIGINS = [
    "https://*.vercel.app",
    "https://*.herokuapp.com",
    "http://localhost:3000",
    "http://localhost:8000",
]

# Development vs Production
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOW_ALL_ORIGINS = False

# Environment-based configuration
if os.environ.get('ALLOWED_HOSTS'):
    ALLOWED_HOSTS.extend(os.environ.get('ALLOWED_HOSTS').split(','))
```

### 4. **Authentication for Swagger UI**

#### Challenge
Swagger UI requiring login but `/accounts/login/` returning 404.

#### Solution
```python
# Add Django auth URLs
urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
]

# Configure Swagger with session auth
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': True,
    'LOGIN_URL': '/accounts/login/',
    'LOGOUT_URL': '/accounts/logout/',
}
```

### 5. **Cross-Platform Setup Scripts**

#### Challenge
Creating setup scripts that work on both Windows and Ubuntu/Linux.

#### Solution
```bash
# Windows batch file (setup_windows.bat)
@echo off
if not exist "venv" (
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirements.txt
python manage.py migrate

# Ubuntu shell script (setup_ubuntu.sh)
#!/bin/bash
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

---

## ❓ Interview Questions & Answers

### 1. **"Explain your Django app structure and why you organized it this way."**

**Answer:**
"I organized the project using Django's app-per-feature approach following the Single Responsibility Principle. Each app handles one specific domain:

- `authentication/` - Only handles user authentication and authorization
- `customers/` - Manages customer profiles, addresses, and relationships
- `products/` - Handles product catalog, variants, and attributes
- `orders/` - Manages order processing and fulfillment
- `inventory/` - Tracks stock levels and movements
- `analytics/` - Provides business intelligence and reporting
- `core/` - Contains shared utilities, middleware, and base classes

This structure provides several benefits:
- **Maintainability**: Each app is focused and easy to understand
- **Scalability**: Apps can be developed independently by different teams
- **Reusability**: Apps can be reused in other projects
- **Testing**: Each app can be tested in isolation"

### 2. **"How did you handle the hierarchical category system?"**

**Answer:**
"I implemented unlimited depth categories using the Materialized Path pattern:

```python
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True)
    path = models.CharField(max_length=255)  # e.g., '1/3/7'
    level = models.PositiveIntegerField(default=0)
```

**Benefits of this approach:**
- **Performance**: Single query to get all ancestors or descendants
- **Flexibility**: Unlimited nesting depth
- **Simplicity**: Easy to understand and maintain

**Alternative approaches considered:**
- **Adjacency List**: Simple but causes N+1 queries for deep hierarchies
- **Nested Sets**: Good for read-heavy workloads but complex updates
- **Closure Table**: Flexible but requires additional table"

### 3. **"Describe your API design decisions."**

**Answer:**
"I followed RESTful API design principles:

**Resource-based URLs:**
```
GET    /api/products/           # List products
POST   /api/products/           # Create product
GET    /api/products/{id}/      # Get specific product
PUT    /api/products/{id}/      # Update product
DELETE /api/products/{id}/      # Delete product
```

**Nested resources for relationships:**
```
GET /api/products/{id}/reviews/    # Product reviews
GET /api/customers/{id}/addresses/ # Customer addresses
```

**Consistent response format:**
```json
{
  "count": 25,
  "next": "http://api.example.com/products/?page=2",
  "previous": null,
  "results": [...]
}
```

**HTTP status codes:**
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Server Error"

### 4. **"How do you handle authentication and authorization?"**

**Answer:**
"I implemented multiple authentication methods:

**Token Authentication for APIs:**
```python
'rest_framework.authentication.TokenAuthentication'
```

**Session Authentication for Swagger UI:**
```python
'rest_framework.authentication.SessionAuthentication'
```

**OAuth2/OpenID Connect for third-party integration:**
```python
'mozilla_django_oidc.contrib.drf.OIDCAuthentication'
```

**Permission System:**
```python
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
```

**Benefits:**
- Flexibility for different client types
- Scalable for microservices architecture
- Security through proper token management"

### 5. **"Explain your database optimization strategies."**

**Answer:**
"I implemented several optimization techniques:

**Query Optimization:**
```python
# Reduce database hits with select_related
products = Product.objects.select_related('category', 'brand')

# Prefetch many-to-many relationships
products = Product.objects.prefetch_related('variants', 'images')
```

**Database Indexing:**
```python
class Meta:
    indexes = [
        models.Index(fields=['category', 'is_active']),
        models.Index(fields=['created_at']),
    ]
```

**Custom QuerySet Managers:**
```python
class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)
    
    def in_stock(self):
        return self.filter(stock_quantity__gt=0)
```

**Caching Strategy:**
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```"

### 6. **"How do you ensure code quality and maintainability?"**

**Answer:**
"I follow several best practices:

**Code Organization:**
- Single Responsibility Principle for apps
- DRY (Don't Repeat Yourself) with base classes
- Clear naming conventions

**Testing Strategy:**
```python
class ProductAPITestCase(APITestCase):
    def test_create_product_valid_data(self):
        # Test with valid data
    
    def test_create_product_invalid_data(self):
        # Test validation errors
    
    def test_product_permissions(self):
        # Test authorization
```

**Documentation:**
- Comprehensive API documentation with Swagger
- Inline code comments for complex logic
- README with setup instructions

**Error Handling:**
```python
def custom_exception_handler(exc, context):
    # Consistent error response format
    return standardized_error_response(exc)
```

**Code Review Process:**
- Git workflow with feature branches
- Pull request reviews
- Automated testing before merging"

### 7. **"Describe a challenging bug you fixed."**

**Answer:**
"**Challenge:** The demo data setup was failing with unique constraint violations when run multiple times.

**Root Cause:** The script was using `objects.create()` which always tries to create new records, causing duplicates.

**Investigation Process:**
1. Analyzed the error traceback
2. Identified the specific constraint violation
3. Reviewed the setup script logic
4. Traced through the category creation hierarchy

**Solution:**
```python
# Before (problematic)
category = Category.objects.create(name=name, parent=parent)

# After (fixed)
category, created = Category.objects.get_or_create(
    name=name,
    parent=parent,
    defaults={'description': description}
)
```

**Additional Improvements:**
- Added transaction management for atomicity
- Improved error messages with context
- Added logging for debugging

**Lessons Learned:**
- Always consider idempotency in setup scripts
- Use appropriate Django ORM methods for the use case
- Test scripts multiple times to catch edge cases"

---

## ⚡ Performance & Optimization

### 1. **Database Optimization**

#### Connection Pooling
```python
# Production database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'MAX_CONNS': 20,
            'OPTIONS': {
                'MAX_CONNS': 20,
            }
        }
    }
}
```

#### Query Optimization Examples
```python
# Bad: N+1 query problem
for product in Product.objects.all():
    print(product.category.name)  # Database hit for each product

# Good: Single query with join
for product in Product.objects.select_related('category'):
    print(product.category.name)  # No additional queries

# Complex optimization
def get_products_with_details():
    return Product.objects.select_related(
        'category', 'brand'
    ).prefetch_related(
        'variants', 'images', 'reviews__customer'
    ).annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    )
```

### 2. **Caching Strategy**

#### Redis Caching
```python
from django.core.cache import cache
from django.views.decorators.cache import cache_page

# Cache expensive queries
def get_featured_products():
    cache_key = 'featured_products'
    products = cache.get(cache_key)
    
    if not products:
        products = Product.objects.filter(
            is_featured=True
        ).select_related('category')[:10]
        cache.set(cache_key, products, timeout=3600)  # 1 hour
    
    return products

# Cache API responses
@cache_page(60 * 15)  # 15 minutes
def product_list(request):
    # This view's response will be cached
    pass
```

### 3. **API Performance**

#### Pagination
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# Custom pagination for large datasets
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000
```

#### Field Selection
```python
# Allow clients to specify fields
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        fields = kwargs.get('context', {}).get('request').query_params.get('fields')
        if fields:
            allowed = set(fields.split(','))
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        super().__init__(*args, **kwargs)
```

---

## 🔒 Security Implementation

### 1. **Input Validation**

#### Model-Level Validation
```python
from django.core.validators import RegexValidator

class Customer(models.Model):
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+254[0-9]{9}$',
                message='Enter a valid Kenyan phone number'
            )
        ]
    )
    
    def clean(self):
        # Custom validation logic
        if self.date_of_birth and self.date_of_birth > timezone.now().date():
            raise ValidationError('Date of birth cannot be in the future')
```

#### Serializer Validation
```python
class ProductSerializer(serializers.ModelSerializer):
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be positive")
        return value
    
    def validate(self, attrs):
        # Cross-field validation
        if attrs.get('compare_at_price', 0) <= attrs.get('price', 0):
            raise serializers.ValidationError(
                "Compare at price must be higher than regular price"
            )
        return attrs
```

### 2. **SQL Injection Prevention**

```python
# Django ORM automatically prevents SQL injection
# Good: Using ORM
products = Product.objects.filter(name__icontains=search_term)

# Bad: Raw SQL without parameterization
cursor.execute(f"SELECT * FROM products WHERE name LIKE '%{search_term}%'")

# Good: Raw SQL with parameters
cursor.execute(
    "SELECT * FROM products WHERE name LIKE %s", 
    [f'%{search_term}%']
)
```

### 3. **Authentication Security**

```python
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Token expiration
from rest_framework.authtoken.models import Token
from django.utils import timezone
from datetime import timedelta

class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')

        # Check token expiration
        if token.created < timezone.now() - timedelta(hours=24):
            raise exceptions.AuthenticationFailed('Token expired.')

        return (token.user, token)
```

### 4. **Permission System**

```python
class IsOwnerOrStaffReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Staff can view all objects.
    """
    
    def has_permission(self, request, view):
        # Authenticated users can view
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for staff
        if request.method in permissions.SAFE_METHODS and request.user.is_staff:
            return True
        
        # Write permissions only to owner
        return obj.user == request.user
```

---

## 🧪 Testing Strategy

### 1. **Unit Tests**

```python
from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.products.models import Product, Category

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic products'
        )
    
    def test_product_creation(self):
        product = Product.objects.create(
            name='Test Product',
            price=99.99,
            category=self.category
        )
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.category, self.category)
    
    def test_negative_price_validation(self):
        with self.assertRaises(ValidationError):
            product = Product(
                name='Test Product',
                price=-10.00,
                category=self.category
            )
            product.full_clean()
```

### 2. **API Tests**

```python
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from apps.products.models import Product

class ProductAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Test Category')
        
    def test_create_product_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'New Product',
            'price': '149.99',
            'category': self.category.id
        }
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
    
    def test_create_product_unauthenticated(self):
        data = {
            'name': 'New Product',
            'price': '149.99',
            'category': self.category.id
        }
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
```

### 3. **Integration Tests**

```python
from django.test import TransactionTestCase
from django.db import transaction

class OrderProcessingIntegrationTest(TransactionTestCase):
    def test_complete_order_flow(self):
        # Create customer
        customer = Customer.objects.create(
            user=self.user,
            phone_number='+254700123456'
        )
        
        # Create product
        product = Product.objects.create(
            name='Test Product',
            price=100.00,
            stock_quantity=10
        )
        
        # Create order
        order = Order.objects.create(customer=customer)
        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=2,
            price=product.price
        )
        
        # Process order
        order.status = 'confirmed'
        order.save()
        
        # Verify inventory update
        product.refresh_from_db()
        self.assertEqual(product.stock_quantity, 8)
        
        # Verify order total
        self.assertEqual(order.total_amount, 200.00)
```

---

## 🚀 Deployment Guide

### Docker Deployment

#### 1. **Create Dockerfile**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Start server
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

#### 2. **Create docker-compose.yml**

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=your-secret-key
      - DATABASE_URL=postgresql://user:password@db:5432/cynthia_store
    depends_on:
      - db
    volumes:
      - ./staticfiles:/app/staticfiles

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=cynthia_store
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

#### 3. **Deploy with Docker**

```bash
# Build and run
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Load demo data
docker-compose exec web python scripts/setup_demo_data.py
```

### Heroku Deployment

#### 1. **Create Procfile**

```bash
echo "web: gunicorn config.wsgi:application --bind 0.0.0.0:\$PORT" > Procfile
```

#### 2. **Install Heroku CLI and Deploy**

```bash
# Install Heroku CLI
# macOS: brew install heroku/brew/heroku
# Ubuntu: sudo snap install heroku --classic

# Login and create app
heroku login
heroku create your-app-name

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Run migrations
heroku run python manage.py migrate
heroku run python scripts/setup_demo_data.py
```

### Vercel Deployment

#### 1. **Create vercel.json**

```json
{
  "version": 2,
  "builds": [
    {
      "src": "config/wsgi.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "config/wsgi.py"
    }
  ],
  "env": {
    "SECRET_KEY": "@secret_key",
    "DEBUG": "False"
  }
}
```

#### 2. **Deploy to Vercel**

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard
# - SECRET_KEY
# - DEBUG=False
# - DATABASE_URL (use external PostgreSQL)
```

### Production Environment Variables

```bash
# Core Django Settings
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database (for external PostgreSQL)
DATABASE_URL=postgresql://user:password@host:port/database

# Or individual database settings
DB_NAME=cynthia_store_prod
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# SMS Configuration (Africa's Talking)
AFRICASTALKING_USERNAME=your_username
AFRICASTALKING_API_KEY=your_api_key
AFRICASTALKING_SENDER=YourSender

# Redis Cache (optional)
REDIS_URL=redis://your-redis-host:6379/1
```

### Production Checklist

#### ✅ **Security**
- [ ] `DEBUG=False` in production
- [ ] Strong `SECRET_KEY` (50+ characters)
- [ ] Proper `ALLOWED_HOSTS` configuration
- [ ] HTTPS redirect enabled
- [ ] Secure cookie settings
- [ ] Database credentials secured

#### ✅ **Performance**
- [ ] Static files served efficiently
- [ ] Database connection pooling
- [ ] Redis caching configured
- [ ] Gzip compression enabled
- [ ] Database indexes optimized

#### ✅ **Monitoring**
- [ ] Logging configured
- [ ] Error tracking setup
- [ ] Performance monitoring
- [ ] Database backup strategy
- [ ] Health check endpoints

### Quick Deployment Commands

```bash
# Check deployment readiness
python manage.py check --deploy

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Test production settings locally
export DEBUG=False
export SECRET_KEY=test-key
python manage.py runserver

# Load demo data
python scripts/setup_demo_data.py
```

---

## 📞 Support & Contact

**Developer**: Cynthia Samuels  
**Email**: cynthy8samuels@gmail.com  
**Phone**: +254798534856  
**Location**: Nairobi, Kenya

### Quick Links
- **Local Development**: http://localhost:8000/
- **API Documentation**: http://localhost:8000/swagger/
- **Admin Panel**: http://localhost:8000/admin/
- **Health Check**: http://localhost:8000/health/

---

**This documentation demonstrates enterprise-level Django development skills, API design principles, security best practices, and production deployment knowledge suitable for backend developer roles.**

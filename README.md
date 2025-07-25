<p align="center">
  <img src="https://img.shields.io/badge/Django-5.2.1-green" alt="Django version"/>&nbsp;
  <img src="https://img.shields.io/badge/Python-3.11-blue" alt="Python version"/>&nbsp;
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" alt="License"/>
</p>

# 🛍️ Cynthia Online Store API

A robust, enterprise-grade Django REST service powering *Cynthia Online Store* for *Savannah Informatics Backend Role Assessment*. Features exhaustive testing, multi-environment deployment automation, and advanced business integrations.

* Test the api endpoints using Swagger or Postman or any other client on your local.

## 🚀 Quick Setup

### Windows Users
```bash
# Run the automated setup script
setup_windows.bat
```

### Ubuntu/Linux Users
```bash
# Run the automated setup script
./setup_ubuntu.sh
```

### Manual Setup (All Platforms)
```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Ubuntu/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create superuser (optional)
python scripts/deploy_setup.py

# 6. Setup demo data (optional)
python scripts/setup_demo_data.py

# 7. Start development server
python manage.py runserver
```

### 🌐 Access Points
- **API Documentation**: http://localhost:8000/swagger/
- **Admin Panel**: http://localhost:8000/admin/ (admin/admin)
- **API Endpoints**: http://localhost:8000/api/

---
![image](https://github.com/user-attachments/assets/6a59d156-3cc6-46fe-a21a-a902eba3e1ee)

![image](https://github.com/user-attachments/assets/f9ece859-ad01-4044-9a85-f9f505f33e7f)


---

## 🚀 Key Features Implemented

### 🔐 Enhanced Authentication System

* User registration, login, logout endpoints
* Token-based authentication (JWT)
* Password change & reset flows
* Profile management
* OAuth2/OpenID Connect support

### 👥 Comprehensive Customer Model

* Extended fields: first\_name, last\_name, gender, age, date\_of\_birth, id\_number
* Validated contact info & multiple addresses
* Business customer support & classification
* Customer preferences & loyalty points
* Financial tracking

### 📦 Advanced Product Management

* Product variants, attributes & types (simple, variable, grouped, digital)
* Brand & SEO fields
* Inventory tracking & low-stock alerts
* Reviews, ratings & image galleries
* Order processing with Africas Talking SMS and email notifications

### 🏷️ Hierarchical Categories

* Unlimited-depth hierarchy (materialized path)
* Category attributes & business rules
* SEO & display configurations

### 💾 Database Flexibility

* PostgreSQL (primary), MySQL (alternative), SQLite (dev)
* Environment-based DB configs

### 📚 API Documentation

* Swagger/OpenAPI UI at `https://cynthia-store.up.railway.app/swagger`
* Interactive testing & schema examples

---

## 🛠️ Setup & Running the Application

### 🐳 Docker (Recommended)

```bash
# Copy env vars & configure
cp .env.example .env
# Start services
docker-compose up -d
```

* **Swagger UI**: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
* **Admin**: [http://localhost:8000/admin/](http://localhost:8000/admin/)
* **API Root**: [http://localhost:8000/api/](http://localhost:8000/api/)

### 🐧 Local Development

```bash
# Install deps
pip install -r requirements.txt
# Migrate & demo data
python manage.py makemigrations && python manage.py migrate
python scripts/setup_demo_data.py
# Run server
python manage.py runserver
```

* **Admin login**: `admin` / `admin123`
* **Test user**: `customer1` / `customer123`

---

## 🛠️ API Endpoints & Examples

> Prefix: `/api/`, Auth: `Authorization: Bearer <token>` (except auth routes)

### 🔐 Authentication

| Endpoint                 |  Method | Description             |
| ------------------------ | :-----: | ----------------------- |
| `/auth/register/`        |   POST  | Register new user       |
| `/auth/login/`           |   POST  | Obtain JWT tokens       |
| `/auth/logout/`          |   POST  | Revoke token            |
| `/auth/profile/`         | GET/PUT | Retrieve/update profile |
| `/auth/change-password/` |   POST  | Change password         |

**Sample: Login**

```http
POST /api/auth/login/
```

```json
{ "username":"customer1", "password":"customer123" }
```

```json
{ "access":"<jwt>", "refresh":"<jwt>" }
```

### 👥 Customers

| Endpoint           |     Method     | Description              |
| ------------------ | :------------: | ------------------------ |
| `/customers/`      |    GET/POST    | List or create customers |
| `/customers/{id}/` | GET/PUT/DELETE | Detail, update, delete   |
| `/customers/me/`   |       GET      | Current user profile     |

### 🏷️ Categories

| Endpoint                        |  Method  | Description               |
| ------------------------------- | :------: | ------------------------- |
| `/categories/`                  | GET/POST | List or create categories |
| `/categories/tree/`             |    GET   | Retrieve full hierarchy   |
| `/categories/{slug}/avg_price/` |    GET   | Average price in category |

### 📦 Products

| Endpoint            |     Method     | Description             |
| ------------------- | :------------: | ----------------------- |
| `/products/`        |    GET/POST    | List or create products |
| `/products/{id}/`   | GET/PUT/DELETE | Retrieve/update/delete  |
| `/products/search/` |       GET      | Search & filter         |

**Sample: Create Product**

```http
POST /api/products/
```

```json
{
  "name":"iPhone 15 Pro",
  "price":"999.99",
  "category":"electronics",
  "sku":"IPH15PRO001",
  "stock_quantity":50
}
```

### 🛒 Orders

| Endpoint             |  Method  | Description                   |
| -------------------- | :------: | ----------------------------- |
| `/orders/`           | GET/POST | List or create orders         |
| `/orders/my_orders/` |    GET   | List current user orders      |
| `/orders/{id}/`      |  GET/PUT | Detail or update order status |

**Sample: Create Order**

```json
POST /api/orders/
{ "items":[{"product_id":1,"quantity":2}] }
```

---

## 🧪 Testing & Coverage

### 🧪 Test Suite Breakdown

* **Unit**: Models, serializers, utils
* **Integration**: API endpoints, DB interactions
* **Acceptance**: End-to-end flows
* **Performance**: Query timings, response benchmarks
* **Security**: Auth, permissions, edge cases

### ▶️ Run Tests

```bash
python scripts/test_runner.py
# or
pytest --cov=./
```

Coverage target: **80%+**

---

## ☸️ Deployment Automation

### Docker

```bash
# Build & run
docker build -t cynthia-store:latest .
docker-compose up -d
```

### Kubernetes (Helm)

```bash
# Build & push image
docker tag cynthia-store:latest your-registry/cynthia-store:latest
docker push your-registry/cynthia-store:latest
# Deploy chart
helm install cynthia-store charts/cynthia-store-chart
```

### CI/CD (GitHub Actions)

* Linting & formatting
* Automated tests & coverage
* Docker build & push
* Helm deployment to staging/production
* Security scanning

---

## 🔒 Security & Monitoring

* Token-based auth, CORS, CSRF protection
* Input validation & sanitization
* SQL injection & XSS prevention
* Rate limiting
* Request logging & error tracking
* Health check & metrics endpoints

---

## 📊 Contact Me

* **Store**: Cynthia Online Store
* **Email**: [cynthy8samuels@gmail.com](mailto:cynthy8samuels@gmail.com)
* **Phone**: +254 798534856
* **Whatsapp**: +254 798534856

---

## 🤝 Contributing

1. Fork & clone repo
2. Create feature branch
3. Commit & open PR
4. CI will run tests & deploy previews

---

## 📄 License

MIT © Cynthia Nyaranda (https://github.com/cynthy-nyaranda)

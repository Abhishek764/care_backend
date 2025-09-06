# 🏥 Healthcare Backend API

<div align="center">

![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)
![DRF](https://img.shields.io/badge/DRF-3.14.0-red.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)
![JWT](https://img.shields.io/badge/JWT-Authentication-orange.svg)
![Security](https://img.shields.io/badge/Security-Hardened-red.svg)

**A secure, scalable healthcare management system built with Django REST Framework**

[Features](#-features) • [Quick Start](#-quick-start) • [API Documentation](#-api-documentation) • [Security](#-security) • [Testing](#-testing)

</div>

---

## 📌 Project Overview

This is a comprehensive **Healthcare Management Backend API** built with modern web technologies. The system provides secure user authentication, patient management, doctor management, and patient-doctor relationship mapping with enterprise-level security features.

### 🎯 Key Highlights
- 🔐 **JWT Authentication** with token rotation
- 🛡️ **Enterprise Security** with rate limiting and input validation
- 👥 **Role-based Access Control** for data isolation
- 📊 **RESTful API** with comprehensive CRUD operations
- 🧪 **Comprehensive Testing** suite included
- 📈 **Production Ready** with security best practices

---

## 🚀 Features

### 🔐 Authentication & Security
- **JWT Token Authentication** with refresh token rotation
- **Rate Limiting** (5 registration attempts/hour, 10 login attempts/hour)
- **XSS Protection** with input sanitization
- **SQL Injection Protection** via Django ORM
- **CORS Configuration** for cross-origin requests
- **Security Headers** (HSTS, X-Frame-Options, Content-Type protection)

### 👥 User Management
- User registration with password confirmation
- Secure login with JWT tokens
- Password validation and strength requirements
- User data isolation and privacy protection

### 🏥 Patient Management
- Complete CRUD operations for patients
- Patient data validation and sanitization
- User-specific patient isolation
- Email and phone number validation

### 👨‍⚕️ Doctor Management
- Doctor profile management
- Specialization tracking
- Public doctor directory
- Professional information validation

### 🔗 Patient-Doctor Mapping
- Assign doctors to patients
- Prevent duplicate mappings
- User-specific mapping access
- Relationship management

---

## 🛠️ Tech Stack

| Category | Technology | Version |
|----------|------------|---------|
| **Backend** | Django | 4.2.7 |
| **API Framework** | Django REST Framework | 3.14.0 |
| **Database** | PostgreSQL / SQLite | 13+ |
| **Authentication** | JWT (SimpleJWT) | 5.3.0 |
| **Security** | CORS Headers, Rate Limiting | Latest |
| **Testing** | Django Test Framework | Built-in |
| **Environment** | Python | 3.11+ |

---

## 📂 Project Structure

```
care_backend/
├── 📁 api/                          # Main API application
│   ├── 📁 migrations/               # Database migrations
│   ├── 📄 models.py                 # Data models (Patient, Doctor, Mapping)
│   ├── 📄 serializers.py            # API serializers with validation
│   ├── 📄 views.py                  # API views with security
│   ├── 📄 urls.py                   # URL routing
│   ├── 📄 permissions.py            # Custom permissions
│   ├── 📄 pagination.py             # API pagination
│   └── 📄 apps.py                   # App configuration
│
├── 📁 care_backend/                 # Django project settings
│   ├── 📄 settings.py               # Main settings with security config
│   ├── 📄 urls.py                   # Root URL configuration
│   ├── 📄 wsgi.py                   # WSGI configuration
│   └── 📄 asgi.py                   # ASGI configuration
│
├── 📄 manage.py                     # Django management script
├── 📄 requirements.txt              # Python dependencies
├── 📄 test_api.py                   # API testing script
├── 📄 security_test.py              # Security testing suite
├── 📄 .env.example                  # Environment variables template
└── 📄 README.md                     # This file
```

---

## ⚙️ Quick Start

### 1. 📥 Clone Repository
```bash
git clone https://github.com/yourusername/healthcare-backend.git
cd healthcare-backend/care_backend
```

### 2. 🐍 Create Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate
```

### 3. 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. 🔧 Environment Configuration
Create a `.env` file in the `care_backend` directory:

```env
# Security Configuration
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (PostgreSQL)
DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# JWT Configuration
ACCESS_TOKEN_LIFETIME_MIN=15
REFRESH_TOKEN_LIFETIME_DAYS=1
```

### 5. 🗄️ Database Setup
```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 6. 🚀 Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

---

## 🔑 API Documentation

### 🔐 Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/auth/register/` | Register new user | ❌ |
| `POST` | `/api/auth/login/` | Login and get JWT tokens | ❌ |
| `POST` | `/api/auth/token/refresh/` | Refresh access token | ❌ |

**Registration Example:**
```json
POST /api/auth/register/
{
    "username": "johndoe",
    "email": "john@example.com",
    "name": "John Doe",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
}
```

### 👥 Patient Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/patients/` | List user's patients | ✅ |
| `POST` | `/api/patients/` | Create new patient | ✅ |
| `GET` | `/api/patients/{id}/` | Get patient details | ✅ |
| `PUT` | `/api/patients/{id}/` | Update patient | ✅ |
| `DELETE` | `/api/patients/{id}/` | Delete patient | ✅ |

**Patient Creation Example:**
```json
POST /api/patients/
{
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane.smith@example.com",
    "date_of_birth": "1990-05-15",
    "phone": "+1234567890"
}
```

### 👨‍⚕️ Doctor Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/doctors/` | List all doctors | ✅ |
| `POST` | `/api/doctors/` | Create new doctor | ✅ |
| `GET` | `/api/doctors/{id}/` | Get doctor details | ✅ |
| `PUT` | `/api/doctors/{id}/` | Update doctor | ✅ |
| `DELETE` | `/api/doctors/{id}/` | Delete doctor | ✅ |

### 🔗 Patient-Doctor Mapping

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/mappings/` | List user's mappings | ✅ |
| `POST` | `/api/mappings/` | Create mapping | ✅ |
| `GET` | `/api/mappings/{patient_id}/` | Get doctors for patient | ✅ |
| `DELETE` | `/api/mappings/{id}/` | Remove mapping | ✅ |

---

## 🛡️ Security Features

### 🔒 Authentication Security
- **JWT Tokens**: Short-lived access tokens (15 minutes)
- **Token Rotation**: Automatic refresh token rotation
- **Rate Limiting**: Protection against brute force attacks
- **Password Validation**: Strong password requirements

### 🛡️ Data Protection
- **XSS Protection**: HTML tag stripping from user input
- **SQL Injection**: Django ORM protection
- **Input Validation**: Comprehensive field validation
- **Data Isolation**: Users can only access their own data

### 🌐 Network Security
- **CORS Configuration**: Controlled cross-origin access
- **Security Headers**: HSTS, X-Frame-Options, Content-Type protection
- **HTTPS Ready**: Production-ready SSL configuration
- **Cookie Security**: HttpOnly, Secure, SameSite protection

### 📊 Rate Limiting
- **Registration**: 5 attempts per IP per hour
- **Login**: 10 attempts per IP per hour
- **API Calls**: 100/hour (anonymous), 1000/hour (authenticated)

---

## 🧪 Testing

### Run API Tests
```bash
# Run comprehensive API tests
python test_api.py
```

### Run Security Tests
```bash
# Run security vulnerability tests
python security_test.py
```

### Run Django Tests
```bash
# Run Django test suite
python manage.py test
```

---

## 📊 API Response Examples

### ✅ Successful Registration
```json
{
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "name": "John Doe"
    },
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

### ✅ Patient List Response
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "date_of_birth": "1990-05-15",
            "phone": "+1234567890",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z"
        }
    ]
}
```

---

## 🚀 Production Deployment

### Environment Variables
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=healthcare_prod
DB_USER=prod_user
DB_PASSWORD=secure_production_password
DB_HOST=your-db-host
DB_PORT=5432
```

### Security Checklist
- [ ] Set strong `SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Use HTTPS in production
- [ ] Set up PostgreSQL database
- [ ] Configure Redis for caching (optional)
- [ ] Set up monitoring and logging
- [ ] Regular security updates

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support

For support, email support@healthcare-api.com or create an issue in the repository.

---

<div align="center">

**Made with ❤️ for Healthcare Management**

[⬆ Back to Top](#-healthcare-backend-api)

</div>
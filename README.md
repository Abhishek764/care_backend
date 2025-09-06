# Healthcare Backend (Django + DRF + PostgreSQL)

## 📌 Project Overview
This project is a backend system for a **Healthcare Application** built using **Django**, **Django REST Framework (DRF)**, and **PostgreSQL**.
It supports **user authentication (JWT)**, **patient management**, **doctor management**, and **patient-doctor mappings**.

---

## 🚀 Features
- User Registration and Login with JWT Authentication
- Patient Management (CRUD)
- Doctor Management (CRUD)
- Patient ↔ Doctor Mapping (with duplicate prevention)
- Role-based access control (patients can only be managed by their creator)

---

## 🛠️ Tech Stack
- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT (using `djangorestframework-simplejwt`)
- **Testing:** Django Test Framework, DRF APITestCase
- **Containerization:** Docker + Docker Compose (optional)

---

## 📂 Project Structure

You're right, I apologize for that! I provided the content directly instead of within a markdown code block.

Here is the content formatted as a markdown code block for a README.md file:

Code snippet

# Healthcare Backend (Django + DRF + PostgreSQL)

## 📌 Project Overview
This project is a backend system for a **Healthcare Application** built using **Django**, **Django REST Framework (DRF)**, and **PostgreSQL**.
It supports **user authentication (JWT)**, **patient management**, **doctor management**, and **patient-doctor mappings**.

---

## 🚀 Features
- User Registration and Login with JWT Authentication
- Patient Management (CRUD)
- Doctor Management (CRUD)
- Patient ↔ Doctor Mapping (with duplicate prevention)
- Role-based access control (patients can only be managed by their creator)

---

## 🛠️ Tech Stack
- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT (using `djangorestframework-simplejwt`)
- **Testing:** Django Test Framework, DRF APITestCase
- **Containerization:** Docker + Docker Compose (optional)

---

## 📂 Project Structure

care_backend/
├── api/
│   ├── migrations/
│   ├── init.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   └── test.py
│
├── care_backend/
│   ├── init.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── manage.py
├── requirements.txt
├── .env
├── docker-compose.yml
└── .gitignore
└── README.md


---

## ⚙️ Setup Instructions

### 1. Clone Repository
```bash
git clone [https://github.com/yourusername/healthcare-backend.git](https://github.com/yourusername/healthcare-backend.git)
cd healthcare-backend
2. Create Virtual Environment
Bash

python -m venv .venv
source .venv/bin/activate   # On Linux/Mac
.venv\Scripts\activate      # On Windows
3. Install Dependencies
Bash

pip install -r requirements.txt
4. Configure Database
Update .env with your PostgreSQL credentials:

DB_NAME=healthcare_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your_secret_key
DEBUG=True
5. Run Migrations
Bash

python manage.py migrate
6. Run Server
Bash

python manage.py runserver
🔑 API Endpoints
Authentication
POST /api/auth/register/ → Register new user

POST /api/auth/login/ → Obtain JWT tokens

POST /api/auth/refresh/ → Refresh JWT token

Patients
GET /api/patients/ → List patients

POST /api/patients/ → Create patient

PUT /api/patients/{id}/ → Update patient

DELETE /api/patients/{id}/ → Delete patient

Doctors
GET /api/doctors/ → List doctors

POST /api/doctors/ → Create doctor

PUT /api/doctors/{id}/ → Update doctor

DELETE /api/doctors/{id}/ → Delete doctor

Patient-Doctor Mapping
GET /api/mappings/ → List mappings

POST /api/mappings/ → Create mapping

DELETE /api/mappings/{id}/ → Remove mapping
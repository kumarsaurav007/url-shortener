# URL Shortener API

A production-ready URL Shortener REST API built with Django REST Framework. The application allows users to register and authenticate using JWT, create shortened URLs, redirect users through short codes, and track URL analytics.

## 🚀 Live Demo

**Live Application:**
https://url-shortener-s04n.onrender.com/

**API Base URL:**
https://url-shortener-s04n.onrender.com/api/

---

## ✨ Features

* User registration
* JWT authentication
* JWT token refresh
* Create shortened URLs
* Redirect using short URLs
* Retrieve and manage shortened URLs
* URL analytics
* PostgreSQL database
* Redis caching
* Celery background task processing
* Celery Beat scheduled tasks
* Django REST Framework
* Dockerized application
* Production deployment on Render

---

## 🛠️ Tech Stack

| Technology            | Purpose                         |
| --------------------- | ------------------------------- |
| Python                | Backend programming language    |
| Django                | Web framework                   |
| Django REST Framework | REST API development            |
| PostgreSQL            | Production database             |
| Redis                 | Cache and Celery message broker |
| Celery                | Background task processing      |
| Celery Beat           | Scheduled background tasks      |
| JWT                   | API authentication              |
| Docker                | Containerization                |
| Gunicorn              | Production WSGI server          |
| Render                | Cloud deployment                |

---

## 📁 Project Structure

```text
url-shortener/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── celery.py
│
├── shortener/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   └── tasks.py
│
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🔐 Authentication

The API uses JWT authentication.

### Register

```text
POST /api/auth/register/
```

### Login

```text
POST /api/auth/login/
```

### Refresh Token

```text
POST /api/auth/token/refresh/
```

Authenticated requests use:

```text
Authorization: Bearer <access_token>
```

---

## 🔗 URL Shortening

### Create Short URL

```text
POST /api/urls/
```

The authenticated user can submit a long URL and receive a shortened URL containing a unique short code.

### Short URL Redirect

```text
GET /<short_code>/
```

Example:

```text
https://url-shortener-s04n.onrender.com/abc123/
```

The request is redirected to the original URL associated with the short code.

---

## 📊 URL Analytics

### Get URL Details

```text
GET /api/urls/<id>/
```

### Get URL Analytics

```text
GET /api/urls/<id>/analytics/
```

Analytics can be used to track activity associated with a shortened URL.

---

## 🐳 Running with Docker

Clone the repository:

```bash
git clone <your-github-repository-url>
cd url-shortener
```

Build and start the containers:

```bash
docker compose up --build
```

The application runs on:

```text
http://localhost:8000/
```

The Docker setup includes services for the Django application, PostgreSQL, Redis, Celery worker, and Celery Beat.

---

## ⚙️ Environment Variables

Create a `.env` file for local development.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=your-postgresql-database-url

REDIS_URL=redis://redis:6379
```

For production, environment variables are configured through the deployment platform rather than committing secrets to Git.

---

## ☁️ Deployment

The application is containerized using Docker and deployed on Render.

Production architecture:

```text
Client
   │
   ▼
Render
   │
   ▼
Gunicorn
   │
   ▼
Django REST Framework
   │
   ├── PostgreSQL
   │
   ├── Redis
   │
   └── Celery
```

The production Docker container uses Gunicorn:

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

Static files are collected during the Docker image build.

---

## 🧪 API Testing

The API can be tested using:

* Django REST Framework Browsable API
* Postman
* cURL

Example API base URL:

```text
https://url-shortener-s04n.onrender.com/api/
```

---

## 🔒 Security

* JWT-based authentication
* Production secrets stored as environment variables
* PostgreSQL used for production data
* Redis used for caching/background task infrastructure
* Django security middleware enabled
* Production deployment uses Gunicorn

---

## 📌 Main API Endpoints

| Method | Endpoint                    | Description              |
| ------ | --------------------------- | ------------------------ |
| POST   | `/api/auth/register/`       | Register a user          |
| POST   | `/api/auth/login/`          | Obtain JWT tokens        |
| POST   | `/api/auth/token/refresh/`  | Refresh access token     |
| POST   | `/api/urls/`                | Create a short URL       |
| GET    | `/api/urls/<id>/`           | Get URL details          |
| GET    | `/api/urls/<id>/analytics/` | Get URL analytics        |
| GET    | `/<short_code>/`            | Redirect to original URL |
| GET    | `/admin/`                   | Django admin             |

---

## 📄 License

This project is intended for learning, development, and portfolio purposes.

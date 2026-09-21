# Expense Splitter API

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-REST_Framework-092E20)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)
![License](https://img.shields.io/badge/License-MIT-green)

A production-oriented **REST API for managing shared group expenses**, built with **Django REST Framework**.

Expense Splitter allows users to create groups, manage members, record expenses, track individual contributions, and calculate how expenses are distributed among group members.

The project focuses on practical backend engineering concepts including **RESTful API design, JWT authentication, authorization, relational database modeling, business logic, PostgreSQL, Redis, Celery, Docker, API documentation, and development profiling**.

---

## 📑 Table of Contents

- [Features](#-features)
- [Tech Stack](#️-tech-stack)
- [Architecture](#️-architecture)
- [Domain Model](#️-domain-model)
- [Authorization Flow](#-authorization-flow)
- [API Overview](#-api-overview)
- [API Documentation](#-api-documentation)
- [Quick Start](#-quick-start)
- [Running Tests](#-running-tests)
- [Celery & Redis](#-celery--redis)
- [Django Silk](#-django-silk)
- [Project Structure](#-project-structure)
- [Environment & Security](#-environment--security)
- [Common Docker Commands](#-common-docker-commands)
- [Future Improvements](#-future-improvements)
- [Current Project Status](#-current-project-status)
- [License](#-license)
- [Author](#-author)

---

## ✨ Features

### 🔐 Authentication

* Custom user registration and authentication
* JWT-based authentication with SimpleJWT
* Access and refresh token support
* Protected API endpoints
* Authenticated user-specific resources

### 👥 Group Management

* Create expense groups
* Group creator automatically becomes the group administrator
* Add and remove members from groups
* Prevent duplicate group memberships
* View groups the authenticated user belongs to
* Group-specific member management

### 💸 Expense Management

* Create expenses inside a group
* Track who paid an expense
* Store expense amount and description
* View group expenses
* Update and delete expenses
* Validate group membership
* Group-level authorization

### 🧮 Expense Splitting & Balances

The system tracks how shared expenses break down between group members:

* Total group expenses
* Individual contributions
* Individual expense shares (split equally between members by default — adjust this note if your implementation supports unequal/percentage splits)
* Amount owed by each member
* Amount receivable by each member
* Group-level financial summary via a dedicated `summary` endpoint

Expense-share calculation is handled through the application's business logic instead of exposing unnecessary public CRUD endpoints.

### 🔒 Authorization

Custom permission classes control access based on:

* Authentication status
* Group membership
* Group administrator privileges

This prevents users from accessing or modifying resources belonging to unrelated groups.

### 📚 API Documentation

Interactive API documentation is generated using:

* OpenAPI
* drf-spectacular
* Swagger UI
* ReDoc

### 🐳 Docker

The application is containerized using Docker and Docker Compose. The development environment includes the required backend infrastructure: Django, PostgreSQL, Redis, and Celery.

### ⚡ Background Tasks

Celery is integrated for asynchronous background processing, with Redis used as the message broker.

### 🔍 Development Profiling

Django Silk is integrated to inspect request performance, database queries, query execution time, and request/response behavior.

---

## 🛠️ Tech Stack

| Technology                | Purpose                         |
| -------------------------- | -------------------------------- |
| **Python**                | Backend programming             |
| **Django**                | Web framework                   |
| **Django REST Framework** | REST API development            |
| **PostgreSQL**            | Relational database             |
| **SimpleJWT**              | JWT authentication               |
| **Redis**                 | Message broker / infrastructure |
| **Celery**                 | Background task processing       |
| **Docker**                 | Application containerization     |
| **Docker Compose**         | Multi-container development      |
| **drf-spectacular**        | OpenAPI documentation            |
| **Django Silk**            | Development profiling            |
| **Postman**                | API testing                      |
| **REST Client**            | API testing                      |

---

## 🏗️ Architecture

```text
                         Client
                           │
                           ▼
                  Django REST API
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
      Authentication               Permissions
             │                           │
             └─────────────┬─────────────┘
                           │
                           ▼
                    Business Logic
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
             PostgreSQL             Redis
                                     │
                                     ▼
                                  Celery
                                     │
                                     ▼
                              Background Tasks
```

---

## 🗃️ Domain Model

```text
                           User
                            │
             ┌──────────────┴──────────────┐
             │                             │
             ▼                             ▼
     GroupMembership                    Expense
             │                             │
             ▼                             │
           Group ──────────────────────────┘
             │
             ▼
        ExpenseShare
```

**Core Models**

| Model | Description |
|---|---|
| `User` | An authenticated application user |
| `Group` | An expense-sharing group; its creator becomes the administrator |
| `GroupMembership` | Links a user to a group; a user can belong to multiple groups |
| `Expense` | An expense recorded inside a group (payer, amount, description, timestamp) |
| `ExpenseShare` | An individual member's share of a given expense |

---

## 🔑 Authorization Flow

```text
                 Authenticated User
                         │
                         ▼
                Is Group Member?
                   │         │
                  Yes        No
                   │         │
                   ▼         ▼
                Allowed    Denied
                   │
                   ▼
            Is Group Admin?
               │       │
              Yes      No
               │       │
               ▼       ▼
        Admin Actions  Member Actions
```

This allows different operations to be restricted according to a user's role within a group.

---

## 📡 API Overview

Base URL:

```text
http://localhost:8000/api/
```

### Authentication

```http
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/refresh/
```

### Groups

```http
GET    /api/groups/
POST   /api/groups/

GET    /api/groups/{id}/
PUT    /api/groups/{id}/
PATCH  /api/groups/{id}/
DELETE /api/groups/{id}/
```

### Group Members

```http
POST   /api/groups/{group_id}/members/
DELETE /api/groups/{group_id}/members/{id}/
```

### Expenses

```http
GET    /api/groups/{group_id}/expenses/
POST   /api/groups/{group_id}/expenses/

GET    /api/groups/{group_id}/expenses/{id}/
PUT    /api/groups/{group_id}/expenses/{id}/
PATCH  /api/groups/{group_id}/expenses/{id}/
DELETE /api/groups/{group_id}/expenses/{id}/
```

### Group Summary / Balances

```http
GET /api/groups/{group_id}/summary/
```

Returns the group's financial summary — total expenses, per-member contributions, and who owes whom.

> The routes above reflect the project's actual implementation. Update this table if you rename or restructure any endpoints.

---

## 📚 API Documentation

The project uses **drf-spectacular** to generate an OpenAPI schema. After starting the application:

| Docs | URL |
|---|---|
| Swagger UI | `http://localhost:8000/api/schema/swagger-ui/` |
| ReDoc | `http://localhost:8000/api/schema/redoc/` |

Swagger UI can be used to explore and interact with the API during development.

---

## 🚀 Quick Start

The recommended way to run the project is with **Docker Compose**.

### Prerequisites

* [Git](https://git-scm.com/)
* [Docker](https://www.docker.com/)
* Docker Compose

You do **not** need to install Python, PostgreSQL, or Redis separately — Docker handles all of it.

### 1. Clone the repository

```bash
git clone  https://github.com/Habib-1/expense-splitter-api.git
cd expense_splitter
```

### 2. Create the environment file

```bash
cp .env.example .env
```

On Windows, manually create a `.env` file and copy the variables from `.env.example`.

Example configuration:

```env
DEBUG=True

SECRET_KEY=your-secret-key

POSTGRES_DB=expense_splitter
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0
```

> Never commit your real `.env` file to GitHub.

### 3. Build and start the project

```bash
docker compose up -d --build
```

This builds the Django image and starts PostgreSQL, Redis, the Django app, and Celery.

```bash
docker compose ps
```

### 4. Run database migrations

```bash
docker compose exec app python manage.py migrate
```

> Replace `web` with your actual service name if it differs in `docker-compose.yml`.

### 5. Create a superuser

```bash
docker compose exec app python manage.py createsuperuser
```

### 6. Access the application

| Service | URL |
|---|---|
| API root | `http://localhost:8000/` |
| Swagger UI | `http://localhost:8000/api/schema/swagger-ui/` |
| ReDoc | `http://localhost:8000/api/schema/redoc/` |
| Django Admin | `http://localhost:8000/admin/` |
| Django Silk | `http://localhost:8000/silk/` |

---

## 🧪 Running Tests

```bash
docker compose exec app pytest
```

Run with coverage:

```bash
docker compose exec app pytest --cov=.
```

The API has also been manually tested during development using Postman, the VS Code REST Client, and Swagger UI, covering JWT authentication, group/membership flows, permission handling, expense CRUD, and authorization failures.

---

## ⚡ Celery & Redis

Celery is integrated for asynchronous background task processing, with Redis as the message broker.

```text
                  Django
                    │
                    │ enqueue task
                    ▼
                  Redis
                    │
                    ▼
              Celery Worker
                    │
                    ▼
             Background Task
```

This allows potentially time-consuming operations to run outside the normal HTTP request-response cycle.

---

## 🔍 Django Silk

Django Silk is used during development for application profiling. It provides visibility into HTTP requests, response times, SQL queries, query execution time, and overall request performance — useful for catching N+1 query problems and slow endpoints before they reach production.

Dashboard: `http://localhost:8000/silk/`

---

## 📁 Project Structure

```text
expense_splitter/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── ...
│
├── users/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── ...
│
├── groups/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   └── ...
│
├── expenses/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   ├── services.py
│   └── ...
│
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── .env.example
├── .gitignore
└── README.md
```

---

## 🔐 Environment & Security

Sensitive configuration is kept outside the source code using environment variables:

* `.env` for local secrets
* `.env.example` for configuration reference
* `.gitignore` for sensitive/local files
* JWT authentication
* Permission-based authorization
* Database constraints
* Protected API endpoints

---

## 🔄 Common Docker Commands

| Action | Command |
|---|---|
| Start | `docker compose up -d` |
| Start and rebuild | `docker compose up -d --build` |
| Stop | `docker compose down` |
| View running containers | `docker compose ps` |
| View all logs | `docker compose logs -f` |
| View Django logs | `docker compose logs -f web` |
| Open Django shell | `docker compose exec web bash` |
| Run a Django management command | `docker compose exec web python manage.py <command>` |

---

## 🧪 Future Improvements

* **Automated testing** — expand pytest/pytest-django coverage: API integration, permission, authentication, and expense-splitting edge-case tests
* **Redis caching** — cache group/expense summaries, add invalidation and query optimization
* **Celery Beat** — scheduled tasks for periodic processing, reminders, and maintenance
* **Notifications** — new expense, group activity, and settlement reminders (email)
* **Advanced analytics** — spending trends, contribution stats, settlement history
* **Frontend dashboard** — a client app for groups, expenses, and settlement visualization
* **Production deployment** — CI/CD, Gunicorn, Nginx, monitoring, centralized logging

---

## 📌 Current Project Status

**Core backend — Completed:** JWT authentication, user/group/membership management, group-level authorization, expense CRUD, expense-sharing logic, PostgreSQL, Redis, Celery, Docker Compose, OpenAPI docs (Swagger/ReDoc), Django Silk profiling, manual API testing.

**Planned:** Expanded pytest suite, Redis caching, Celery Beat, notifications, advanced analytics, CI/CD, production deployment.

---

## 📸 Screenshots

> Add screenshots to a `docs/` folder and reference them below.

```markdown
![Swagger UI](docs/swagger.png)
![Expense API](docs/expense-api.png)
![Django Silk](docs/silk.png)
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Habibur Rahman**
Backend Developer | Python | Django | Django REST Framework

Interested in building scalable and maintainable backend systems with Python and Django.

- GitHub: [github.com/Habib-1](https://github.com/Habib-1)
- LinkedIn: [linkedin.com/in/habiburrahman-habib](https://www.linkedin.com/in/habiburrahman-habib/)

---

### ⭐ If You Find This Project Useful

Feel free to explore the repository, review the API documentation, and experiment with the API locally.

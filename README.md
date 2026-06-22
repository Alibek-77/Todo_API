# ✅ Task Manager API

A production-ready REST API for managing tasks with JWT authentication, role-based access control, and full Docker support.

## Features

- JWT authentication — register, login, protected endpoints
- Personal tasks — each user sees only their own tasks
- Role-based access — admin can view all tasks
- Dockerized — runs anywhere with one command
- Tested — pytest test suite included

## Tech Stack

- **FastAPI** — REST API framework
- **PostgreSQL** — relational database
- **SQLAlchemy** — ORM
- **python-jose + bcrypt** — JWT auth and password hashing
- **Docker + docker-compose** — containerization
- **pytest** — testing

## Project Structure

```
task_manager/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── dependencies.py
│   ├── settings.py
│   └── routers/
│       ├── auth.py
│       └── todos.py
├── tests/
│   ├── test_auth.py
│   └── test_tasks.py
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── requirements.txt
└── README.md
```

## Quick Start

**1. Clone the repository**
```bash
git clone https://github.com/your-username/task-manager-api.git
cd task-manager-api
```

**2. Create `.env` file**
```
DATABASE_URL=postgresql://postgres:postgres@db:5432/task_db
SECRET_KEY=your_secret_key_minimum_32_characters_long
ALGORITHM=HS256
ACCESS_TOKEN_MINUTES=30
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=task_db
```

**3. Run with Docker**
```bash
docker-compose up --build
```

API is available at `http://localhost:8000`

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/auth/register` | Register new user | — |
| POST | `/auth/login` | Login, get JWT token | — |
| GET | `/todos/` | Get my tasks | ✓ |
| POST | `/todos/` | Create task | ✓ |
| PATCH | `/todos/{id}` | Update task | ✓ |
| DELETE | `/todos/{id}` | Delete task | ✓ |
| GET | `/todos/all` | Get all tasks | Admin |

## Authentication

```bash
# register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@mail.com", "password": "password123"}'

# login
curl -X POST http://localhost:8000/auth/login \
  -d "username=user@mail.com&password=password123"

# use token
curl http://localhost:8000/todos/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Running Tests

```bash
# with Docker
docker-compose run api pytest tests/ -v

# locally
pytest tests/ -v
```

## Documentation

Swagger UI: `http://localhost:8000/docs`
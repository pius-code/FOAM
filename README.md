# FOAM - Backend Development Learning Project

## What This App Is About

[TODO: Add project description here]

---

## Table of Contents

1. [Learning Journey Overview](#learning-journey-overview)
2. [Project Architecture](#project-architecture)
3. [Day 1: Docker & FastAPI Basics](#day-1-docker--fastapi-basics)
4. [Day 2: Database Migrations with Alembic](#day-2-database-migrations-with-alembic)
5. [Day 3: Task Scheduling with Celery](#day-3-task-scheduling-with-celery)
6. [Project Structure](#project-structure)
7. [Development Roadmap](#development-roadmap)

---

## Learning Journey Overview

This repository documents my journey learning backend development with FastAPI, PostgreSQL, Docker, and asynchronous task processing. Each section below explains **what** I built, **why** it matters, and **where** to find it in the codebase.

---

## Project Architecture

### Tech Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy
- **Migration Tool**: Alembic
- **Task Queue**: Celery + Celery Beat
- **Message Broker**: Redis
- **Containerization**: Docker + Docker Compose

### Services Running

- `foam_web` - FastAPI application (port 8000)
- `foam_postgres` - PostgreSQL database (port 5432)
- `foam_redis` - Redis message broker (port 6379)
- `foam_celery_worker` - Celery worker for background tasks
- `foam_celery_beat` - Celery Beat scheduler for cron-like jobs

---

## Day 1: Docker & FastAPI Basics

### What I Learned

**Backend & Databases**

- Understood the difference between NoSQL (MongoDB) and SQL (PostgreSQL) databases
- Learned that MongoDB uses direct clients while PostgreSQL requires an ORM/driver
- Decided to use Docker instead of local PostgreSQL installation (more professional, portable)

**Docker & Docker Compose**

- Docker runs services in isolated containers
- Docker Compose orchestrates multiple containers (app + database)
- Learned the difference between `build: .` (custom image) and `image: postgres:15` (official prebuilt image)

### What I Built

**Simple FastAPI Application**

```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def welcome():
    return {"message": "Welcome to FOAM 🎉"}
```

📁 **Location**: `src/main.py`

**Docker Configuration**

**Dockerfile** - Installs Python, dependencies, copies code, starts the app
📁 **Location**: `Dockerfile`

**docker-compose.yml** - Defines services (web + db), manages networking and volumes
📁 **Location**: `docker-compose.yml`

**run.sh** - Entry point script that runs migrations and starts the server
📁 **Location**: `run.sh`

### Key Files Created

| File                 | Purpose                                | Location              |
| -------------------- | -------------------------------------- | --------------------- |
| `Dockerfile`         | Defines app container build process    | `/Dockerfile`         |
| `docker-compose.yml` | Orchestrates multi-container setup     | `/docker-compose.yml` |
| `requirements.txt`   | Python dependencies                    | `/requirements.txt`   |
| `run.sh`             | Startup script for migrations + server | `/run.sh`             |
| `main.py`            | FastAPI application entry point        | `/src/main.py`        |

### Lessons Learned

✅ Start simple: use `uvicorn` before `Gunicorn`, use `python:3.12` before `slim` images
✅ Fixed typo: `psycorg2-binary` → `psycopg2-binary`
✅ FastAPI auto-generates API docs at `/docs` (Swagger UI)

### Running the App

```bash
# Start all services
docker compose up --build

# Access the app
http://localhost:8000

# View API documentation
http://localhost:8000/docs
```

---

## Day 2: Database Migrations with Alembic

### What I Learned

**Alembic - Database Version Control**

- Alembic manages database schema changes safely without data loss
- Works like "Git for your database structure"
- Automatically generates SQL migration scripts from SQLAlchemy models

**SQLAlchemy ORM**

- Instead of writing raw SQL, define Python classes as database tables
- Alembic detects model changes and generates migrations
- Can query using Python: `session.query(User).filter(User.id == 68).first()`

### What I Built

**User Model Example**

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
```

📁 **Location**: `src/db/models/users.py`

**Alembic Configuration**

- Connected Alembic to PostgreSQL via `DATABASE_URL`
- Pointed to SQLAlchemy models (`Base.metadata`)
- Configured automatic model detection

📁 **Location**: `alembic.ini`, `migrations/env.py`

### Key Concepts

**Migration Workflow**

1. Define/modify SQLAlchemy models
2. `alembic revision --autogenerate -m "description"` - Creates migration
3. `alembic upgrade head` - Applies migration to database

**Model Discovery Problem & Solution**

❌ **Problem**: Alembic only sees imported models - unmanageable with 100+ models

✅ **Solution**: Auto-import all models using `__init__.py`

```python
# src/db/models/__init__.py
from .users import User
from .reminders import Reminder
# ... etc
```

📁 **Location**: `src/db/models/__init__.py`

### Key Files Created

| File                 | Purpose                   | Location                     |
| -------------------- | ------------------------- | ---------------------------- |
| `alembic.ini`        | Alembic configuration     | `/alembic.ini`               |
| `env.py`             | Alembic environment setup | `/migrations/env.py`         |
| `models/__init__.py` | Auto-imports all models   | `/src/db/models/__init__.py` |
| `users.py`           | User model example        | `/src/db/models/users.py`    |

### Important Notes

⚠️ **Don't automate `alembic revision`** - it's a developer decision
✅ **Automate `alembic upgrade head` in `run.sh`** - applies migrations on startup

---

## Day 3: Task Scheduling with Celery

### What I Learned

**Cron Jobs - The Basics**

- Scheduled tasks that run automatically at fixed times/intervals
- Like setting server reminders without manual intervention
- Example: send reports daily at midnight, clean logs every hour

**Celery - Distributed Task Queue**

- Runs background jobs asynchronously (outside main app)
- Processes tasks sent by the application or scheduler
- Uses Redis as message broker for task communication

**Celery Beat - The Scheduler**

- Celery's "cron system" for Python
- Sends tasks to workers at scheduled intervals
- Configured via `beat_schedule` in Celery app

### How It Works

```
┌─────────────┐      ┌─────────┐      ┌────────────────┐      ┌──────────┐
│ Celery Beat │─────>│  Redis  │─────>│ Celery Worker  │─────>│ Database │
│ (Scheduler) │      │ (Broker)│      │   (Executor)   │      │          │
└─────────────┘      └─────────┘      └────────────────┘      └──────────┘
     |                                          |
     | Every 60s                                | Runs task
     | Send task                                | Updates DB
```

### What I Built

**Celery App Configuration**

```python
celery_app = Celery(
    "foam",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["src.worker.tasks.scheduler.task_scheduler"]
)

celery_app.conf.beat_schedule = {
    "foam_worker": {
        "task": "src.worker.tasks.scheduler.task_scheduler.schedule_reminder",
        "schedule": 60.0,  # Every 60 seconds
    }
}
```

📁 **Location**: `src/worker/celery_app.py`

**Task Function**

```python
@celery_app.task
def schedule_reminder():
    # Check database for due reminders
    # Execute reminders that are due now
    pass
```

📁 **Location**: `src/worker/tasks/scheduler/task_scheduler.py`

### Key Concepts

**Dynamic Scheduling Pattern**
Instead of creating one Beat task per reminder:

- Create ONE universal Beat task that runs every minute
- That task checks the database for due reminders (e.g., "Monday 6PM")
- Only executes reminders that are due now
- ✅ New reminders = new DB entries (no code changes needed)

**Task Registration**
Celery must know where tasks are defined:

```python
include=["src.worker.tasks.scheduler.task_scheduler"]
```

### Debugging the "Unregistered Task" Error

❌ **Error**: `Received unregistered task of type 'src.worker.tasks...'`

**Root Cause**: Celery worker couldn't find the task

✅ **Solution**:

1. Ensure correct import path in `include=[]`
2. Match task name exactly: `"src.worker.tasks.scheduler.task_scheduler.schedule_reminder"`
3. Verify task is decorated with `@celery_app.task`

### Key Files Created

| File                | Purpose                              | Location                                        |
| ------------------- | ------------------------------------ | ----------------------------------------------- |
| `celery_app.py`     | Celery configuration & Beat schedule | `/src/worker/celery_app.py`                     |
| `task_scheduler.py` | Scheduled task functions             | `/src/worker/tasks/scheduler/task_scheduler.py` |
| `reminder_task.py`  | Reminder execution logic             | `/src/worker/tasks/reminder_task.py`            |

### Running Celery

```bash
# Start all services (includes Celery worker + Beat)
docker compose up --build

# View Celery logs
docker compose logs foam_celery_worker
docker compose logs foam_celery_beat
```

---

## Project Structure

```
FOAM/
├── src/
│   ├── main.py                    # FastAPI entry point
│   ├── api/
│   │   └── routes/               # API endpoints
│   ├── db/
│   │   ├── models/               # SQLAlchemy models
│   │   │   ├── __init__.py       # Auto-imports all models
│   │   │   └── users.py          # Example: User model
│   │   └── database.py           # Database connection
│   └── worker/
│       ├── celery_app.py         # Celery configuration
│       └── tasks/
│           ├── scheduler/
│           │   └── task_scheduler.py  # Scheduled tasks
│           └── reminder_task.py  # Task implementations
├── migrations/                    # Alembic migrations
│   └── env.py                    # Alembic environment
├── Dockerfile                     # App container definition
├── docker-compose.yml            # Multi-container orchestration
├── requirements.txt              # Python dependencies
├── run.sh                        # Startup script
└── alembic.ini                   # Alembic configuration
```

---

## Development Roadmap

### Completed ✅

- [x] Set up FastAPI + Docker + PostgreSQL
- [x] Configure Alembic migrations
- [x] Set up Celery + Celery Beat + Redis
- [x] Fix task registration issues
- [x] Design dynamic scheduling system

### TODO 📝

- [ ] Change uvicorn setup to Gunicorn with multiple workers
- [ ] Automate model imports for Alembic (no manual specification in `__init__.py`)
- [ ] Implement reminder creation API
- [ ] Build notification system
- [ ] Add user authentication

---

## Key Learnings

### Philosophy

> **Start simple, understand fully, then optimize.**

- Use basic tools first (uvicorn → Gunicorn, python:3.12 → slim)
- Understand WHY each piece exists before moving forward
- Skip complexity (like Alembic) until fundamentals are clear

### Best Practices Discovered

1. **Docker**: Prefer Docker over local installations (portable, consistent)
2. **Migrations**: Never automate `alembic revision`, only `upgrade head`
3. **Task Queues**: One dynamic task > Many hardcoded tasks
4. **Structure**: Organize by domain (api/, db/, worker/) not by type

---

## Resources & Documentation

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Celery Documentation](https://docs.celeryq.dev/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Docker Compose Reference](https://docs.docker.com/compose/)

---

_This README serves as both project documentation and a learning journal. Each section reflects real problems solved and lessons learned during development._

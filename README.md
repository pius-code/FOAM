# docker and devops stuff

[ ] change the uvicorn set up to gunicorn with multiple workers
[x] Task for tomorrow 17th Sept - understand and set up databases, alembic, spin up a simple repo , model , create and store in database
[ ] auotmate imports for the alembic models, no need to manually specify them using **init**.py version

Notes

# Summary of Progress So Far (FastAPI + Postgres + Docker Journey)

Backend & Databases

You learned that for backend development, you can choose between databases (MongoDB, Postgres, etc.).

MongoDB can be used directly via a client, while Postgres usually requires an ORM/driver.

Postgres can run locally, but you don’t need to install it if you use Docker (preferred, more professional).

Docker & Docker Compose

Docker runs services in containers.

Docker Compose orchestrates multiple containers (your FastAPI app + Postgres DB).

For the app, you used build: . (custom image).

For the DB, you used image: postgres:15 (official prebuilt image).

Project Setup

Dockerfile: installs Python, dependencies from requirements.txt, copies code, and starts the app via run.sh.

docker-compose.yml: defines two services:

web: FastAPI app, builds from Dockerfile, exposes port 8000.

db: Postgres, official image, exposes port 5432, persistent storage via volumes.

requirements.txt: includes FastAPI, psycopg2-binary, etc. (fixed typo psycorg2-binary).

run.sh: runs Alembic migrations (skipped for now) and starts the app using Gunicorn+Uvicorn or just Uvicorn.

FastAPI Basics

Created a simple main.py:

from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def welcome():
return {"message": "Welcome to FOAM 🎉"}

Learned how to run locally with uvicorn main:app --reload.

Understood that FastAPI auto-generates /docs (Swagger UI).

Errors & Fixes

Build failed due to misspelling psycorg2-binary → corrected to psycopg2-binary.

Learning Philosophy

Start simple: use uvicorn instead of Gunicorn, python:3.12 base image instead of slim to avoid extra setup.

Skip Alembic for now until fundamentals are clear.

You want to fully understand why each piece exists before moving forward. #

### Day 2 , what I have learnt

Alembic & Migrations

Alembic helps you apply database schema changes safely without losing data.

You:

alembic init migrations → sets up migration folder.

Configure it to connect to Postgres (via DATABASE_URL).

Point it to SQLAlchemy models (Base.metadata).

Run alembic revision --autogenerate -m "message" to create migration scripts.

Run alembic upgrade head to apply them.

If nothing changed in models → Alembic creates an empty migration file.

Don’t automate revision in run.sh (only upgrade head), because revision is a developer decision.

SQLAlchemy ORM

Instead of writing raw SQL, you define models (Python classes).

Example:

class User(Base):
**tablename** = "users"
id = Column(Integer, primary_key=True, index=True)
username = Column(String(50), nullable=False, index=True)
email = Column(String(100), unique=True, nullable=False, index=True)

Alembic inspects these models and generates SQL migrations for you.

You can still use SQLAlchemy ORM to query like:

session.query(User).filter(User.id == 68).first()

How Alembic sees models

Alembic only sees models that are imported into Python.

That’s why in env.py you had to import them (e.g., from src.db.models.users import User).

Problem: becomes unmanageable with 100s of models.

Solutions:

Create models/**init**.py that imports all models.

Use dynamic import (pkgutil + importlib) to automatically import every model in the folder.

👉 Big picture:

Alembic = database version control.

SQLAlchemy = define tables & query with Python.

Together → you rarely touch raw SQL directly.

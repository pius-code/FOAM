# docker and devops stuff

[ ] change the uvicorn set up to gunicorn with multiple workers
[ ] Task for tomorrow 17th Sept - understand and set up databases, alembic, spin up a simple repo , model , create and store in database

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

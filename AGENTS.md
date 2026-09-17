# Open Anime Tracker - Agent Guide

## Project Overview

Open Anime Tracker is a full-stack web application for tracking anime ratings. It consists of:

- **Backend**: Python 3.11 Flask API with SQLAlchemy, Flask-RESTful, Flask-Login, and Redis sessions
- **Frontend**: React 18 + TypeScript (Material-UI) in `oat-frontend/`
- **Database**: PostgreSQL 15 (via Docker/Podman containers)
- **Caching/Sessions**: Redis (via Docker/Podman containers)
- **Migrations**: Alembic
- **Package management**: `uv` (lockfile `uv.lock`) for backend, `npm` for frontend

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.11.x |
| uv | Latest |
| Node.js | 20.x |
| Docker or Podman | For PostgreSQL + Redis containers |

### Backend Setup (uv)

```sh
uv sync        # install dependencies from uv.lock into .venv
uv run flask --app main run --debug
```

Use `uv run` for other commands (e.g. `uv run alembic upgrade head`, `uv run pytest`).

---

## Environment Variables

Create a `.env` file in the root directory:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
PG_PORT=5432
SALT=123
REDIS_IP=127.0.0.1
SECRET_KEY=your-secret-key-here
```

Generate a `SECRET_KEY` with:

```sh
python -c 'import secrets; print(secrets.token_hex())'
```

---

## Starting the App

### 1. Start Infrastructure (PostgreSQL + Redis + Adminer)

```sh
# Docker
docker compose up -d
# Podman (drop-in, same compose file)
podman compose up -d
```

This starts:
- **PostgreSQL** on port `5432`
- **Redis** on port `6379`
- **Adminer** (DB admin UI) on port `5557` — visit `http://localhost:5557`

### 2. Run Database Migrations

```sh
alembic upgrade head
```

### 3. Start the Flask Backend

```sh
flask --app main run --debug
```

The API will be available at `http://localhost:5000`.

### 4. Start the Frontend

```sh
cd oat-frontend
npm install   # only needed on first setup
npm start
```

The frontend will open at `http://localhost:3000`.

---

## Stopping the App

```sh
# Stop infrastructure
docker compose down
# ...or with Podman
podman compose down

# Stop backend: Ctrl+C in the terminal running flask

# Stop frontend: Ctrl+C in the terminal running npm start
```

---

## Project Structure

```
.
├── main.py                 # Flask app entry point
├── config.py               # Server configuration (SQLAlchemy, Redis, sessions)
├── const.py                # Runtime constants loaded from .env
├── database.py             # DB engine and session setup
├── alembic.ini             # Alembic migration config
├── docker-compose.yml      # PostgreSQL, Redis, Adminer containers
│
├── alembic/                # Migration scripts
│   ├── env.py
│   └── versions/
│
├── routes/                 # Flask route blueprints
│   ├── anime.py            # Anime CRUD + search routes
│   ├── kitsu.py            # Kitsu import routes
│   ├── list.py             # List routes (deprecated, not registered)
│   ├── login.py            # Auth routes
│   └── user.py             # User routes
│
├── db_models/              # SQLAlchemy models
│   ├── base.py
│   ├── anime.py
│   ├── users.py
│   ├── ratings.py
│   ├── seasons.py
│   ├── list.py
│   └── invites.py
│
├── authentication/         # User auth logic
│   └── user.py
│
├── common_funcs/           # Shared utilities
│   ├── db_funcs.py
│   ├── kitsu.py            # Kitsu API helpers + season import service
│   └── login.py
│
├── project_exceptions/     # Custom exceptions
│   ├── exceptions.py
│   └── ...
├── enums/                  # Enum definitions
│   └── db_enums.py
│
├── data_pull.py            # One-off Kitsu data pull script
├── data_store.py           # One-off Kitsu data store script
│
├── .agents/                # Agent rules (per-module conventions)
├── .spec-workflow/         # Spec-driven development workflow docs
│
├── oat-frontend/           # React + TypeScript frontend
│   ├── src/
│   ├── public/
│   └── package.json
│
└── tests/
```

---

## Alembic Migrations

```sh
# Create a new migration after changing models
alembic revision --autogenerate -m "description"

# Apply pending migrations
alembic upgrade head

# Revert one migration
alembic downgrade -1
```

---

## Development Notes

- The backend loads DB credentials and runtime constants from environment variables via `const.py`; `SECRET_KEY` is read directly from `os.environ` in `config.py`
- Sessions are stored in Redis — make sure the Redis container is running
- CORS allows `http://localhost:3000` with credentials (see `main.py`)
- The frontend uses `react-scripts` (Create React App) — no separate build step required in dev mode
- No backend tests currently exist in the `tests/` directory

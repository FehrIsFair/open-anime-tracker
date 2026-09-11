# Technical Standards

## Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Backend | Python | 3.11.x |
| Backend Framework | Flask | — |
| ORM | SQLAlchemy | — |
| Auth | Flask-Login | — |
| Caching | Redis | — |
| Frontend | React | 18 |
| Frontend Language | TypeScript | — |
| UI Library | Material-UI | — |
| HTTP Client | Axios | — |
| Database | PostgreSQL | 15 (via Docker) |
| Migrations | Alembic | — |
| Dev Infra | Docker Compose | — |

## Coding Standards

### Backend (Python)
- Use Flask blueprints for route organization (see `routes/anime.py`, `routes/user.py`)
- Use `make_response` from Flask for consistent response handling
- Use SQLAlchemy ORM models from `db_models/` for all database access
- Custom exceptions in `project_exceptions/` for error handling
- Database credentials loaded from environment variables via `const.py`
- Enum validation using project enums from `enums/db_enums.py`
- Use `session.commit()` explicitly after mutations

### Frontend (TypeScript)
- Use React functional components with hooks
- TypeScript interfaces for all data models (see `oat-frontend/src/Models/`)
- Material-UI for all UI components
- Axios instance from `oat-frontend/src/BackendRequests/base.ts` for all API calls
- Auth context from `oat-frontend/src/context/auth_context` for auth state
- React Router v6 for navigation with `<BrowserRouter>` and `<Routes>`
- Text formatting via shared config in `oat-frontend/src/TextFormating/`

## Naming Conventions
- Backend: snake_case for variables, functions, files; PascalCase for classes
- Frontend: camelCase for variables/functions; PascalCase for components/interfaces
- File names: kebab-case for new files (consistent with existing `nav-header.tsx`, etc.)

## API Patterns
- Routes use blueprint registration (see `routes/anime.py` for pattern)
- Responses use `make_response(dict, status_code)`
- Error responses return `{'message': 'Error description'}` with appropriate status codes
- Frontend API calls grouped by domain in `BackendRequests/`

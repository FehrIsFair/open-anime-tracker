# Project Structure

## Directory Layout

```
.
├── main.py                 # Flask app entry point
├── config.py               # Server configuration
├── const.py                # Runtime constants from .env
├── database.py             # DB engine and session setup
├── auth.py                 # Authentication utilities
├── docker-compose.yml      # PostgreSQL + Redis + Adminer
│
├── alembic/                # Database migration scripts
│   ├── env.py
│   └── versions/
├── routes/                 # Flask route blueprints
│   ├── anime.py            # Anime CRUD routes
│   ├── kitsu.py            # Kitsu import routes
│   ├── login.py            # Login routes
│   ├── user.py             # User routes
│   └── list.py             # List routes
├── db_models/              # SQLAlchemy ORM models
│   ├── base.py             # Base class with make_json
│   ├── anime.py            # Anime model
│   ├── seasons.py          # Seasons model
│   ├── users.py            # User model
│   ├── ratings.py          # Rating model
│   ├── list.py             # List model
│   └── invites.py          # Invite model
├── authentication/         # User auth logic
├── common_funcs/           # Shared utilities
├── project_exceptions/     # Custom exceptions
├── enums/                  # Enum definitions
│   └── db_enums.py
│
├── oat-frontend/           # React + TypeScript frontend
│   ├── src/
│   │   ├── App.tsx          # Main app with routes
│   │   ├── Pages/           # Page components
│   │   ├── Header/          # Navigation components
│   │   ├── BackendRequests/ # API call modules (Axios)
│   │   ├── Models/          # TypeScript interfaces
│   │   ├── context/         # React contexts (auth)
│   │   └── TextFormating/   # Shared text style configs
│   └── package.json
│
├── tests/                  # Test files (minimal)
└── .spec-workflow/         # Spec workflow docs
```

## Key Patterns

### Route Blueprints
Routes are organized in `routes/` as Flask blueprints. Each file defines a blueprint and registers routes:
```python
# routes/anime.py
anime_routes = Blueprint('anime', __name__)
@anime_routes.route('/anime/search', methods=['GET'])
def search_anime(): ...
```

### Frontend Pages
Pages are components in `oat-frontend/src/Pages/`. Each page is a separate file and route in `App.tsx`.

### API Request Modules
API calls are grouped by domain in `oat-frontend/src/BackendRequests/` using a shared axios instance from `base.ts`.

### Models
- Backend models: `db_models/` with `make_json()` for serialization
- Frontend models: `oat-frontend/src/Models/` with TypeScript interfaces

### Navigation
Routes defined in `App.tsx` using React Router `<Routes>`. Auth pages guarded by `AuthRoute`.

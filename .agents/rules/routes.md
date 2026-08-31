# Routes Rules

## Purpose

The `routes/` directory contains all Flask API endpoint definitions. Each route file defines a set of related endpoints grouped under a single URL prefix, registered as blueprints in `main.py`.

## Conventions

- **Always use `Blueprint`** — `flask_classful.FlaskView` should be avoided. See `list.py` as a deprecated example.
- **Always apply `@cross_origin(origin="*")` on route functions** — required for proper communication with the React dev server. The global CORS config in `main.py` alone is not sufficient.
- **Return consistent response format** — use `make_response(jsonify({...}), status_code)` for all JSON responses.
- **Handle errors explicitly** — wrap DB operations in `try/except` and return `{'Message': '...', status_code}`.
- **Use the shared `session`** from `database.py` — do not import `db.session` from SQLAlchemy directly.

## Route Files

### [`routes/anime.py`](../routes/anime.py)

Handles CRUD for anime entries. Uses the `anime` blueprint prefix.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/anime` | List all anime |
| `POST` | `/anime/create` | Create a new anime |
| `PATCH` | `/anime/edit` | Edit an existing anime |
| `DELETE` | `/anime/delete` | Soft-delete an anime |

**Dependencies:**
- [`db_models/anime.py`](../db_models/anime.py) — `Anime` model (link to `rules/models.md` for details)
- [`enums/db_enums.py`](../enums/db_enums.py) — `AnimeType`, `ReviewStatus`
- [`project_exceptions/exceptions.py`](../project_exceptions/exceptions.py) — `InvalidEnumException`

**Key patterns:**
- `get_anime_type()` and `get_review_type()` validate enum inputs — throws `InvalidEnumException` on invalid values.
- `edit_anime` uses a diff-based approach: only keys in `request_json['diffs']` are applied.
- `create_anime` skips `title`, `_type`, and `status` from kwargs (handled explicitly) and passes the rest through.

### [`routes/user.py`](../routes/user.py)

Handles user management (listing, creation, updates, deletion). Uses the `user` blueprint prefix.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/user` | List all users |
| `POST` | `/user/create` | Create a new user |
| `PATCH` | `/user/update_pw` | Update user password |
| `PATCH` | `/user/edit` | Edit user profile (verifies password first) |
| `DELETE` | `/user/delete` | Soft-delete a user |

**Dependencies:**
- [`db_models/users.py`](../db_models/users.py) — `User` model
- `flask_bcrypt` — password hashing
- [`helper_funcs.py`](../helper_funcs.py) — `bcrypt` (imported locally to avoid circular imports)

**Key patterns:**
- Passwords are hashed with `flask_bcrypt.generate_password_hash()` during creation.
- `edit_user` requires the current password in `json['password']` before allowing updates.
- `delete_user` sets `deleted_at` (soft delete) instead of removing the record.

> **Naming inconsistency:** `update_pw` and `edit` are swapped in purpose relative to their names. `update_pw` updates the password; `edit` updates profile fields. Consider renaming for clarity.

### [`routes/login.py`](../routes/login.py)

Handles authentication (login, logout, auth check). Uses the `auth` blueprint prefix.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/login` | Authenticate user and create session |
| `POST` | `/auth/logout` | Invalidate user session |
| `POST` | `/auth/auth_check` | Verify an existing session |

**Dependencies:**
- [`db_models/users.py`](../db_models/users.py) — `User` model
- `flask.session` — session storage (backed by Redis)
- `bcrypt` — password verification
- `uuid.uuid4` — session token generation

**Known issue:** User sessions are not properly persisted on login — refreshing the page clears auth. The fix requires a `Set-Cookie` header in the login response to ensure the session cookie is sent to the browser. This is tracked as a future task.

**Key patterns:**
- Login creates a session entry: `session[user.username] = uuid4()`.
- Logout removes the session entry for the user.
- Auth check looks up the session by the passed cookie UUID and returns the username.

### [`routes/list.py`](../routes/list.py)

Handles user anime lists (watchlist tracking). Uses `FlaskView` (class-based) — **deprecated pattern**.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/list/<int:_id>` | Get a list by ID |
| `POST` | `/list` | Add anime to a user's list |
| `DELETE` | `/list` | Remove anime from a user's list |

**⚠️ Not yet registered in `main.py` — blocked on session persistence fix.** Once auth is resolved (see `login.py` section), this file will be converted from `FlaskView` to `Blueprint` and registered alongside the other routes.

Current outdated patterns:
- Uses `FlaskView` instead of `Blueprint`.
- Imports `db.session` from SQLAlchemy directly instead of using the project's `session` from `database.py`.
- Returns raw tuples `(status_code, body)` instead of `make_response(...)`.
- Has a variable shadowing bug: `anime = anime = db.session.query(...)` on line 22.
- The `index` method always returns `404`.

## Registration

All active blueprints are registered in [`main.py`](../main.py):

```python
app.register_blueprint(anime_routes)  # prefix: /anime
app.register_blueprint(user_routes)   # prefix: /user
app.register_blueprint(login_routes)  # prefix: /auth
```

The `list.py` `FlaskView` was intended to be registered via `ListView.register(app)` but is currently commented out in `__init__.py`.

## Response Format Standards

All routes should follow this response pattern:

```python
from flask import make_response, jsonify

# Success
make_response(jsonify({'data': [...]}), 200)

# Error
make_response(jsonify({'Message': 'Description'}), status_code)
```

| Status Code | Use |
|-------------|-----|
| 200 | Success |
| 401 | Unauthorized / invalid credentials |
| 404 | Not found |
| 409 | Conflict (e.g., duplicate) |
| 500 | Internal server error |

> Use other status codes as appropriate for situations not covered by the table above.

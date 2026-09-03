# DB Models — Rules

This directory contains all SQLAlchemy ORM models for Open Anime Tracker.

## Conventions

### Inheritance & Base

- **Always** inherit from `Base` (`db_models.base.Base`), which extends `sqlalchemy.orm.DeclarativeBase`.
- **Do not** use `SqlAlchemyBase` from `base.py` — it is legacy.

### Table & Column Names

- `__tablename__` must be lowercase, pluralized (e.g. `'users'`, `'anime'`, `'lists'`, `'ratings'`, `'seasons'`, `'invites'`).
- Column names in the DB match the Python attribute names exactly.
- Foreign keys reference **table name.column**, e.g. `ForeignKey('users.id')` — never `User.id`.

### Column Types

| Python type | DB type | Notes |
|---|---|---|
| `Integer` | `INTEGER` | Primary keys, counts, FKs |
| `String` | `VARCHAR` | Text, UUIDs |
| `Float` | `FLOAT` | Ratings, scores |
| `DateTime` | `TIMESTAMP` | Timestamps; use `default=datetime.utcnow()` |
| `Boolean` | `BOOLEAN` | Flags; set `default=False` |
| `JSON` | `JSON` | Arbitrary JSON data |
| `Enum(SomeEnum)` | PostgreSQL enum | Import from `enums.db_enums` |

### `__init__` Pattern

```python
def __init__(self, required_field: int, optional: str = None, **kwargs):
    super().__init__()
    self.required_field = required_field
    for key, value in kwargs.items():
        self.__dict__[key] = value
```

- Call `super().__init__()` **before** setting attributes.
- Set required fields explicitly.
- Use `self.__dict__[key] = value` for optional/extra kwargs (inline `set_values`).
- Generate UUIDs with `uuid.uuid4()`.

### `make_json` Pattern

Override the stub in `Base.make_json()` to serialise a model for API responses:

```python
def make_json(self):
    result = {}
    for key, value in self.__dict__.items():
        match key:
            case '_sa_instance_state':
                continue
            case 'password':
                continue  # never expose secrets
            case _:
                if isinstance(value, Enum):
                    result[key] = value.value
                else:
                    result[key] = value
    return result
```

- Always skip `_sa_instance_state`.
- For enum columns, use `.value`.
- Exclude sensitive fields (e.g. `password`).

### Timestamps

- Use `created_at` and `updated_at` with `default=datetime.utcnow()` for models that need audit trails.
- Use `deleted_at = Column(DateTime, nullable=True)` for soft-delete support.

### Imports Order

```python
from sqlalchemy import Column, Integer, String, Float, Enum, JSON, ForeignKey, DateTime, Boolean
from db_models.base import Base
from enums.db_enums import SomeEnum   # if applicable
import uuid                            # if applicable
from datetime import datetime          # if timestamps
```

## Model Reference

| File | Class | Table | FKs |
|---|---|---|---|
| `anime.py` | `Anime` | `anime` | — |
| `users.py` | `User` | `users` | — |
| `ratings.py` | `Rating` | `ratings` | `→ users.id`, `→ anime.id`, `→ anime.id` (season) |
| `seasons.py` | `Seasons` | `seasons` | `→ anime.id` |
| `list.py` | `List` | `lists` | `→ anime.id`, `→ users.id` |
| `invites.py` | `Invites` | `invites` | `→ users.id` |
| `base.py` | `Base` | — | Declarative base |

## Adding a New Model

1. Create `<snake_case>.py` in `db_models/`.
2. Inherit `Base`, define `__tablename__`, add `id` PK.
3. Add columns with appropriate types.
4. Add `__init__` with required fields, use `__dict__` for optional.
5. Add `make_json()` if the model is returned via API.
6. Import the new model in `alembic/env.py` so Alembic can autogenerate.

## Link to Migrations

Every model change requires a new Alembic migration. See `alembic/.agents/rules.md`.

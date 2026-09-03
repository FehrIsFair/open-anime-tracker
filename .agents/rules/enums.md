# Enums Rules

## Purpose

The `enums/` directory contains Python `enum.Enum` classes that define domain-specific constant sets used across models, routes, and validation logic. They live in [`db_enums.py`](../enums/db_enums.py).

## Current Enums

### `AnimeType`

| Value | Description |
|-------|-------------|
| `show` | Standard TV series episodes |
| `movie` | Feature-length films |

Used by: [`routes/anime.py`](routes/anime.py), [`db_models/anime.py`](../db_models/anime.py)

### `ReviewStatus`

| Value | Description |
|-------|-------------|
| `pending` | Awaiting review |
| `confirmed` | Approved |
| `quarantine` | Flagged for review |

Used by: [`routes/anime.py`](routes/anime.py)

### `SeasonType`

| Value | Description |
|-------|-------------|
| `SEASON` | Standard seasonal anime |
| `ONA` | Online released anime |
| `OVA` | Original video animation |
| `SPECIAL` | Special episodes |

Used by: [`db_models/seasons.py`](../db_models/seasons.py)

## Conventions

- **Use `enum.Enum`** — not `enum.IntEnum` or `enum.StrEnum`. All enum values are strings.
- **Enum members match their string values** — e.g., `AnimeType.show = 'show'`. This keeps serialization trivial (no `.value` or `.name` indirection needed in most places).
- **Never construct enums from raw strings without validation** — always use `get_anime_type()` / `get_review_type()` helper functions in routes, which raise `InvalidEnumException` on invalid input.
- **Add a commented helper pattern** if you need a reverse lookup (value → enum) — see the commented `convert_string_to_anime_enum` in `db_enums.py`.

## Rule: Adding a New Enum

1. **Define it in [`db_enums.py`](../enums/db_enums.py)** alongside related enums.
2. **Give members lowercase string values** matching the member name (unless domain semantics differ, like `SeasonType.SEASON = 'season'`).
3. **Create a validation helper** in the consuming route file (e.g., `get_anime_type()`) that:
   - Accepts a string
   - Returns the matching `enum` member
   - Raises `InvalidEnumException` if no match
4. **Update this rule file** with the new enum's values and usage.

### Anti-patterns

- ❌ Hardcoding string literals instead of referencing enum members
- ❌ Using `if x == 'show'` in routes — use the enum validation helper
- ❌ Mixing enum names and values (e.g., checking `enum_member == 'show'` instead of `enum_member == AnimeType.show`)

## Usage Pattern

```python
from enums.db_enums import AnimeType, ReviewStatus
from project_exceptions.exceptions import InvalidEnumException

# In routes — validate input string → enum
def get_anime_type(type_str: str) -> AnimeType:
    for anime_type in AnimeType:
        if anime_type.value == type_str:
            return anime_type
    raise InvalidEnumException(f'Value: {type_str} is not a valid Anime Type')

# Use the enum member
anime_type = get_anime_type(request_json['type'])
```

## Dependencies

- Routes that consume enums → [`rules/routes.md`](routes.md)
- Exceptions triggered by invalid enums → [`rules/project_exceptions.md`](project_exceptions.md)

# Project Exceptions Rules

## Purpose

The `project_exceptions/` directory contains custom exception classes that represent domain-specific error conditions. They live in `exceptions.py`.

## Current Exceptions

| Exception | Purpose |
|-----------|---------|
| `InvalidEnumException` | Raised when a value doesn't match any valid enum member (e.g., invalid `AnimeType` or `ReviewStatus` input). |

## Rule: When to Add a Custom Exception

Add a new custom exception **only when** the condition meets **both** of these criteria:

1. **It represents a specific, recognizable error condition** that callers need to handle differently from generic failures (e.g., `InvalidEnumException` → caught to return a clear 4xx vs. a blind 500).
2. **It is caught explicitly in at least one route** — if no route distinguishes it from a bare `Exception` or `ValueError`, it doesn't earn its own class yet.

If the condition is something the Python runtime already provides (e.g., `KeyError`, `TypeError`, `ValueError`) and the route catches it generically, **do not** create a custom wrapper.

### Anti-patterns

- ❌ One exception per line of code / every `except` clause
- ❌ Custom exceptions that are never caught — they're just `Exception` with a name
- ❌ Nested exception classes (e.g., `class NotFoundException(InvalidEnumException)`)

## Usage Pattern

```python
from project_exceptions.exceptions import InvalidEnumException

# Raise with a descriptive message
raise InvalidEnumException(f'Value: {input} is not a valid Anime Type')

# Catch explicitly in routes
except InvalidEnumException:
    return make_response(jsonify({'Message': '...'}), 400)
```

## Dependencies

- Routes that catch custom exceptions → [`rules/routes.md`](routes.md)
- Enum types that trigger `InvalidEnumException` → [`rules/enums.md`](enums.md)

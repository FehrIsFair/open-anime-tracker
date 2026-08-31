# Enums & Models — Type System Rules

## Overview

Type definitions live in two directories:

| Directory | Purpose |
|-----------|---------|
| `Enums/` | Enum-like arrays for dropdowns, radio groups, and select components |
| `Models/` | TypeScript interfaces and `to_json` serialization helpers |

---

## Rule: Enums Are Select Options, Not TypeScript Enums

Enums in this project are **plain JavaScript arrays** of `{ label, value }` objects — not TypeScript `enum` declarations. They exist solely as data sources for UI components (e.g., `<Select menu_options={AnimeTypeEnum} />`).

```tsx
// ✅ Correct — plain array for UI consumption
export const AnimeTypeEnum = [
  { label: 'Movie', value: 'movie' },
  { label: 'Show', value: 'show' }
]

// ❌ Wrong — don't use TypeScript `enum` here
// export enum AnimeType { Movie = 'movie', Show = 'show' }
```

### Enum Conventions

- **Naming**: Use PascalCase with an `Enum` or descriptive suffix (`AnimeTypeEnum`, `StatusEnum`, `ContentRating`)
- **Structure**: Always `{ label: string, value: string }` — never `{ label, value }` where value is a number
- **Export style**: Export as `const` arrays, not as default exports
- **Grouping**: Related enums belong in the same file (e.g., `AnimeType`, `Status`, `ContentRating` all in `AnimeType.tsx`)

---

## Rule: Models Define Interfaces — Not Classes

Interfaces in this project define the shape of data going to/from the backend. They are **not classes** and **not types** — always use `interface` for object shapes.

```ts
// ✅ Correct — interface for object shapes
export interface Anime {
  title: string;
  jp_title: string;
  _type: string;
  seasons: number;
  rating: number | null;
  episodes: number;
  desc: string;
  status: string;
  nsfw: boolean;
  content_rating: string;
}

// ❌ Wrong — don't use `type` for object shapes that need `to_json`
// export type Anime = { ... }
```

### Interface Conventions

- **Naming**: PascalCase, matching the domain entity (`Anime`, `User`, `Login`, `Auth`)
- **Nullability**: Use `string | null` for fields that may be absent; never use `any` as a fallback type
- **Backend alignment**: Property names must match the backend model exactly (snake_case for DB columns, e.g. `content_rating`, `jp_title`)
- **Default export**: Export the interface as default for convenient named imports, and export any helpers separately

```ts
// ✅ Correct
export interface User {
  username: string | null
  email: string | null
  password: string | null
}

export const to_json = (object: User): any => {
  return _(object).toJSON()
}

export default User
```

---

## Rule: `to_json` Is Mandatory for Backend Payloads

Every model file that sends data to the backend must export a `to_json` helper using lodash's `_.toJSON()`. This handles undefined fields and converts Date objects to serializable strings.

```ts
// ✅ Correct — model exports to_json
export const to_json = (object: Anime): any => {
  return _(object).toJSON()
}

// ✅ Correct — use to_json when posting
import Anime, { to_json } from '../Models/anime'
import engine from '../BackendRequests/base'

const payload = to_json(anime)
await engine.post('/anime/create', payload)

// ❌ Wrong — sending raw object without serialization
await engine.post('/anime/create', anime)

// ❌ Wrong — using JSON.stringify instead of to_json
await engine.post('/anime/create', JSON.stringify(anime))
```

### `to_json` Conventions

- Always use lodash `_(object).toJSON()`, never `JSON.stringify()`
- Import both the interface (for typing) and `to_json` (for serialization) together
- The model file is the **single source of truth** for serialization — don't duplicate `to_json` elsewhere

---

## Rule: Import from Models — Don't Duplicate Interfaces

Interfaces are defined once in `Models/` and imported wherever needed. Never redeclare an interface inline in a component or route file.

```ts
// ✅ Correct — import from Models
import Anime from '../Models/anime'
import { Login } from '../Models/user'

// ❌ Wrong — duplicate interface in component
interface Anime {
  title: string
  // ...
}
```

---

## Rule: No `any` in Model Interfaces — Use `null` or Union Types

Avoid `any` in model definitions. If a field can be multiple types, use an explicit union:

```ts
// ✅ Correct — explicit union
rating: number | null

// ❌ Wrong — `any` hides type errors
rating: number | any
```

---

## Rule: Single-File Enum Groups

Each file in `Enums/` should group related enums (e.g., all anime-related enums in one file). If a group has more than 3–4 enums, split into a separate file.

```
Enums/
├── AnimeType.tsx     # AnimeTypeEnum, StatusEnum, ContentRating (all anime form-related)
└── <new>.tsx         # New group when needed
```

---

## Adding a New Model

When adding a new model:

1. **Create the interface** in the appropriate file under `Models/`
2. **Export `to_json`** using `_(object).toJSON()`
3. **Export default** the interface and named export `to_json`
4. **Add `null`-safe types** — no `any`
5. **Import in components** instead of defining inline
6. **Use `to_json`** when serializing payloads to the backend
7. **No `debugger`** — remove before finishing
8. **No `redirect()`** — use `useNavigate()` instead

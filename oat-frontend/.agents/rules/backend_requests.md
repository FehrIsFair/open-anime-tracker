# Backend Requests — API Layer Rules

## Location

All API calls live in `oat-frontend/src/BackendRequests/`:

| File | Exports | Purpose |
|------|---------|---------|
| `base.ts` | `engine` (Axios instance) | Shared HTTP client with `baseURL: http://localhost:5000` |
| `anime.ts` | `animePost`, `animeGet` | Anime CRUD endpoints |
| `user.ts` | `userCreate`, `login` | User auth endpoints |

## Rule: Use `engine` — Never Hardcode URLs

The `engine` instance from `base.ts` is the **only** way to make API calls:

```ts
import engine from "../BackendRequests/base"

// ✅ Correct
const res = await engine.get("/anime")
await engine.post("/auth/login", payload)

// ❌ Wrong — hardcodes the backend URL
import axios from "axios"
axios({ method: "POST", url: "http://localhost:5000/user/create", data: payload })
```

Every API endpoint path is relative to `baseURL` already set on `engine`. If a new endpoint is needed and it's on the same backend, **do not** import axios and create a new URL.

## Rule: Always Return the Response

API functions must return their response so the caller can handle success and error:

```ts
// ✅ Correct — returns the promise
export const animeGet = async (): Promise<any> => {
  const { data } = await engine.get("/anime")
  return data
}

// ❌ Wrong — fire-and-forget, no return value
export const animePost = async (anime: Anime) => {
  engine.post("/anime/create", to_json(anime)).then(...).catch(...)
}
```

## Rule: Use `try/catch` — Never Silent Catches

All API functions must handle errors explicitly. Silent `.catch(console.log)` swallows errors and makes debugging impossible:

```ts
// ✅ Correct
export const animeGet = async (): Promise<any> => {
  try {
    const { data } = await engine.get("/anime")
    return data
  } catch (err) {
    console.error("Failed to fetch anime:", err)
    throw err
  }
}

// ❌ Wrong — silently swallows errors
engine.post("/anime/create", payload).catch((err) => {
  console.log(err)
})
```

## Rule: No `debugger` Statements

`debugger` statements are development-only and must never ship to production. They have been found in `anime.ts` (line 20). If you add one during debugging, remove it before committing.

## Rule: Consistent Return Types

All async API functions should declare explicit return types:

```ts
export const animeGet = async (): Promise<any> => { ... }
export const animePost = async (anime: Anime): Promise<any> => { ... }
export const login = async (login: Login): Promise<any> => { ... }
```

## Rule: Use `to_json` for Payloads

When sending data to the backend, serialize with the `to_json` helper from `Models/`:

```ts
import { to_json } from "../Models/anime"
import engine from "../BackendRequests/base"

const payload = to_json(anime)
await engine.post("/anime/create", payload)
```

## Rule: Prefer Existing API Functions

If a function already exists in `BackendRequests/` that matches the needed endpoint, import and use it — do not duplicate the call:

```ts
// ✅ Correct
import { animeGet } from "../BackendRequests/anime"
const data = await animeGet()

// ❌ Wrong — duplicate the call in the page component
const { data } = await engine.get("/anime")
```

## Adding a New API Endpoint

When adding a new endpoint to the backend:

1. **Add a function** in the appropriate file (`anime.ts` or `user.ts`), or create a new file if the domain is distinct.
2. **Use `engine`** with a relative URL path.
3. **Return the response** with an explicit type.
4. **Wrap in `try/catch`** and log errors with `console.error`.
5. **No `debugger`** — remove before finishing.
6. **Update the table** at the top of this file if creating a new file.

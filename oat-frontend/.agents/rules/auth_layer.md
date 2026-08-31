# Authentication — Auth Layer Rules

## Overview

The frontend uses cookie-based auth managed via `universal-cookie`:

| Component | Role |
|-----------|------|
| `context/auth_context.tsx` | React Context — holds `user` state, provides `setLogin` |
| `extentsions/helper_funcs.ts` | Exports `cookie_handler` (`new Cookies()`) for reading/writing cookies |
| `Header/nav-header.tsx` | Shows/hides nav links based on `context.user` |
| Page components (`AddAnime`, `GetAnime`) | Auth gate: `context.user != null ? ... : <Navigate to="/signin" />` |

## Rule: `engine` Must Send Cookies

The `engine` Axios instance in `base.ts` must have `withCredentials: true` so that cookies set on login are included in every subsequent request to the backend:

```ts
// base.ts
import axios from 'axios'

const engine = axios.create({
  baseURL: 'http://localhost:5000',
  withCredentials: true  // ← required for cross-origin cookie support
})
export default engine
```

Without this, the frontend sets a cookie on login but never sends it on subsequent API calls — effectively logging the user out on every request.

## Rule: Auth Flow Steps

Every login flow must follow this sequence:

1. **POST to login endpoint** via `engine.post('/auth/login', loginPayload)`
2. **Extract response data** — the backend returns `[uuid, email, username]`
3. **Browser automatically stores** the `oat` cookie from the `Set-Cookie` response header — no manual cookie manipulation needed
4. **Call `context.setLogin({ username, email, password: null })`** to update React state
5. **Navigate** using the `useNavigate()` hook — never use `redirect()` from `react-router-dom` (it is not a hook and does nothing in v6)

```tsx
// ✅ Correct login handler
const submitForm = async () => {
  const loginData: Login = { email, password }
  const res = await engine.post('/auth/login', loginData)
  const [uuid, email, username] = res.data


  context.setLogin({ username, email, password: null })
  navigate('/add-anime')
}
```

## Rule: Auth Gate Pattern

Authenticated routes must gate access by checking `context.user`:

```tsx
// ✅ Correct — inline gate
const AuthenticatedPage = () => {
  const { user } = useContext(AuthContext)

  if (!user) return <Navigate to="/signin" />

  return <Box>/* page content */</Box>
}
```

## Rule: Use `engine` for Auth — Not Raw Axios

Auth-related API calls must go through `engine`, never direct `axios`:

```ts
// ✅ Correct
import engine from "../BackendRequests/base"
const res = await engine.post('/auth/login', data)

// ❌ Wrong
import axios from 'axios'
axios({ url: 'http://localhost:5000/auth/login', data })
```

## Rule: Use Existing Auth API Functions

The `login` function in `BackendRequests/user.ts` exists but is **unused** — page components call `engine.post` directly. When using `BackendRequests/user.ts` functions:

- Import from the module, not from `axios`
- The `login` function returns a `Promise<any>` — handle the response the same way as the inline version above

```ts
// Either use engine directly (current pattern) — or use the module:
import { login } from "../BackendRequests/user"
const res = await login({ email, password })
```

## Rule: Remove `debugger` Statements

`debugger` exists in `auth_context.tsx` (line 16). Remove all `debugger` statements before committing — they halt the app in the browser.

## Rule: Use `useNavigate` — Not `redirect`

`redirect()` from `react-router-dom` is **not** a hook and does not perform navigation in React Router v6. Always use `useNavigate()`:

```tsx
// ✅ Correct
import { useNavigate } from 'react-router-dom'
const navigate = useNavigate()
navigate('/add-anime')

// ❌ Wrong
import { redirect } from 'react-router-dom'
redirect('/add-anime') // Does nothing in v6
```

## Backend-frontend Cookie Contract

| Field | Value |
|-------|-------|
| Cookie name | `oat` |
| Cookie value | UUID token (returned by `/auth/login`) |
| Expiry | 8 hours from login time |
| Cookie transport | Automatic via `Set-Cookie` response header |
| Cookie send on requests | Requires `withCredentials: true` on `engine` |

## Adding a New Auth Endpoint

When adding auth-related endpoints:

1. **Use `engine`** with a relative path (e.g., `engine.post('/auth/logout', data)`)
2. **Handle the response** — extract data, update `context.setLogin` if the user state changes
3. **Call a logout endpoint** via `engine.post('/auth/logout')` to invalidate the session server-side
4. **Clear the `oat` cookie** via `cookie_handler.remove('oat')` to remove stale client-side state
5. **Wrap in `try/catch`** and log errors with `console.error`
6. **No `debugger`** — remove before finishing
7. **No `redirect()`** — use `useNavigate()` instead

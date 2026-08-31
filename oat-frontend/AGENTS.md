# Open Anime Tracker - Frontend Guide

## Overview

The frontend is a React 18 + TypeScript application built with Create React App (`react-scripts`) and Material-UI v5 for the component library. It provides a single-page application (SPA) for rating and tracking anime, communicating with the Flask API at `http://localhost:5000`.

---

## Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.2.0 | UI framework |
| TypeScript | 4.9.5 | Type safety |
| Material-UI | 5.15.x | UI component library |
| Emotion | 11.11.x | CSS-in-JS styling (MUI dependency) |
| React Router | 6.29.x | Client-side routing |
| Axios | 1.6.8 | HTTP client |
| Lodash | 4.17.x | Utility functions (`to_json`) |
| universal-cookie | 7.2.x | Cookie-based session management |
| react-scripts | 5.0.1 | Build tooling (Create React App) |

---

## Prerequisites

| Tool | Version |
|------|---------|
| Node.js | 20.x |
| npm | (bundled with Node) |

---

## Starting the Frontend

```sh
cd oat-frontend
npm install   # only needed on first setup or after adding dependencies
npm start
```

The development server runs at `http://localhost:3000` and hot-reloads on file changes.

---

## Building for Production

```sh
npm run build
```

Output goes to `oat-frontend/build/`.

---

## Testing

```sh
npm test
```

Runs Jest in watch mode. Uses React Testing Library for component tests.

---

## Project Structure

```
oat-frontend/
├── public/                    # Static assets
├── src/
│   ├── App.tsx                # Root component: routing, layout, AuthProvider
│   ├── index.tsx              # Entry point: renders App inside StrictMode
│   ├── App.css                # Global styles
│   ├── index.css              # Base CSS (empty)
│   │
│   ├── Pages/                 # Page components (one per route)
│   │   ├── AddAnime.tsx       # Form for creating a new anime entry
│   │   ├── GetAnime.tsx       # Lists all anime cards (auth-gated)
│   │   ├── SignIn.tsx         # Login form
│   │   └── SignUp.tsx         # Registration form
│   │
│   ├── BackendRequests/       # API layer
│   │   ├── base.ts            # Shared Axios instance (baseURL: localhost:5000)
│   │   ├── anime.ts           # Anime-related API calls (create, list)
│   │   └── user.ts            # User-related API calls (create, login)
│   │
│   ├── Models/                # TypeScript interfaces for API data
│   │   ├── anime.ts           # Anime interface + to_json helper
│   │   └── user.ts            # User, Login interfaces + to_json helper
│   │
│   ├── context/               # React Context providers
│   │   └── auth_context.tsx   # AuthContext: user state + setLogin
│   │
│   ├── Header/                # Navigation components
│   │   ├── nav-header.tsx     # AppBar that swaps nav based on auth state
│   │   ├── user-nav.tsx       # Nav links for authenticated users
│   │   └── no-user-nav.tsx    # Nav links for unauthenticated users
│   │
│   ├── FormComps/             # Reusable form components (MUI wrappers)
│   │   ├── InputComp.tsx      # Standard text input
│   │   ├── EmailComponent.tsx # Email input
│   │   ├── PasswordComp.tsx   # Password input
│   │   ├── NumberInput.tsx    # Number input
│   │   ├── TextAreaComp.tsx   # Multi-line text area
│   │   ├── SelectComp.tsx     # Dropdown select
│   │   ├── CheckBoxComp.tsx   # Checkbox
│   │   └── Buttons/
│   │       └── SubmitBtn.tsx  # Form submit button
│   │
│   ├── Enums/                 # Enum-like arrays for selects
│   │   └── AnimeType.tsx      # AnimeTypeEnum, StatusEnum, ContentRating
│   │
│   ├── TextFormating/         # Typography style presets
│   │   └── text_config.ts     # Style objects for h1-h6, p, link, button
│   │
│   ├── extentsions/           # Utility functions (note: "extentsions" is the folder name)
│   │   └── helper_funcs.ts    # cookie_handler (universal-cookie instance)
│   │
│   ├── react-app-env.d.ts     # CRA type declarations
│   ├── reportWebVitals.ts     # Performance monitoring
│   ├── setupTests.ts          # Jest setup
│   └── App.test.tsx           # Component test
│
├── package.json               # Dependencies and scripts
├── tsconfig.json              # TypeScript config (strict mode)
└── .gitignore
```

---

## Routing

All routes are defined in `src/App.tsx`:

| Route | Component | Auth Required |
|-------|-----------|---------------|
| `/` | `MainPage` | No |
| `/add-anime` | `AddAnime` | Yes (redirects to `/signin`) |
| `/get-anime` | `GetAnime` | Yes (redirects to `/signin`) |
| `/signup` | `SignUp` | No |
| `/signin` | `SignIn` | No |
| `*` | Redirect to `/login` | No |

The `<AuthProvider>` wraps everything, providing user state globally.

---

## Architecture Patterns

### API Layer

Backend calls are organized in `BackendRequests/` with two approaches:

1. **`engine` (recommended)** — Pre-configured Axios instance from `base.ts` with `baseURL: http://localhost:5000`. Use `engine.get()`, `engine.post()`, etc.
2. **Direct axios calls** — Hardcoded URLs (used in `user.ts` and `anime.ts` for `userCreate` / `animePost`). Prefer `engine` for new code.

### Data Models

TypeScript interfaces live in `Models/` and define the shape of data exchanged with the API:

- **`Anime`** — `title`, `jp_title`, `_type`, `seasons`, `rating`, `episodes`, `desc`, `status`, `nsfw`, `content_rating`
- **`User`** — `username`, `email`, `password` (nullable fields)
- **`Login`** — `email`, `password` (string)
- **`to_json()`** — Lodash-based serializer used to convert model objects before sending to the API

### State Management

Auth state is managed via React Context (`AuthContext`):

```tsx
// Provider value shape
interface Auth {
  user: User | null;
  setUser: CallableFunction | null;
  setLogin: (user: User) => void;
}
```

Components consume it with `useContext(AuthContext)`. Auth gating is done inline in page components by checking `context.user != null` and rendering `<Navigate>` when unauthenticated.

### Cookies

Session tokens are stored as cookies via `universal-cookie`. The shared `cookie_handler` instance lives in `extentsions/helper_funcs.ts`. On login, a cookie named `oat` is set with a 8-hour expiry.

### Form Components

Custom form inputs wrap MUI components with a consistent interface:

```tsx
interface InputProps {
  id: string;
  label: string;
  value: string | number | boolean;
  set_field: React.Dispatch<React.SetStateAction<string>>;
}
```

This pattern is used across `InputComp`, `EmailComponent`, `PasswordComponent`, `NumberInput`, `TextAreaComp`, and `CheckBoxComp`. Dropdowns use `SelectComp` with `menu_options` accepting enum arrays.

---

## Environment

The frontend connects to the backend at a hardcoded URL: `http://localhost:5000`. This is set in `BackendRequests/base.ts` as the `baseURL` for the Axios instance. For different environments, update this value or add environment variables.

---

## TypeScript Configuration

`tsconfig.json` uses strict mode (`"strict": true`) with the following notable settings:

- `"target": "es5"` — Compilation target
- `"jsx": "react-jsx"` — JSX transform (React 17+)
- `"moduleResolution": "node"` — Node-style module resolution
- `"isolatedModules": true` — Required by react-scripts

---

## Known Issues & Notes

1. **`debugger` statements** — There are `debugger` calls in `auth_context.tsx` (line 16) and `anime.ts` (line 20). These should be removed before production.
2. **Broken redirect in SignIn** — `SignIn.tsx` imports `redirect` from `react-router-dom` (line 12) and calls it (line 38), but this doesn't perform navigation in React Router v6. Use `useNavigate()` hook with `navigate()` instead.
3. **Hardcoded backend URL** — `base.ts` uses a literal `http://localhost:5000`. Consider using `process.env.REACT_APP_API_URL` for environment flexibility.
4. **`extentsions` folder name** — Contains a typo (should be `extensions`). Renaming requires updating all import paths.
5. **`to_json` helper** — Uses `_(object).toJSON()` which relies on Lodash chaining. If an object lacks a `toJSON()` method, this silently returns the original object.
6. **Empty CSS files** — `index.css` is empty. Global styles should go in `App.css`.
7. **No route protection wrapper** — Auth checks are done inline in each page component rather than with a reusable `RequireAuth` route wrapper.

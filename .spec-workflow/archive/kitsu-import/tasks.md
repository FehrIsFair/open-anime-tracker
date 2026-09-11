# Tasks Document

- [x] 1. Create Kitsu API service (`common_funcs/kitsu.py`)
  - File: `common_funcs/kitsu.py` (new)
  - Implement `fetch_and_store_kitsu_anime(kitsu_id: int)` function that:
    1. Calls Kitsu API at `https://kitsu.io/api/edge/anime/{kitsu_id}`
    2. Parses the anime data and creates an `Anime` record
    3. Creates one `Seasons` record (season 1) linked to the new anime
    4. Commits both records in a single transaction
  - Handle errors: Kitsu API unreachable → raise custom exception, 404 → raise custom exception, malformed data → raise custom exception
  - Map Kitsu fields to Anime/Seasons model fields per design
  - Use existing `const.kitsu_api_base`, `const.kitsu_headers`, `database.session`
  - Purpose: Core business logic — fetches Kitsu data and persists it to DB
  - _Leverage: `data_pull.py` (Kitsu API call pattern), `const.py` (API config), `db_models/anime.py`, `db_models/seasons.py`, `enums/db_enums.py`_
  - _Requirements: 1.1, 1.2, 1.3, 1.4_
  - _Prompt: Role: Backend Developer with expertise in Flask and external API integration | Task: Create `common_funcs/kitsu.py` with `fetch_and_store_kitsu_anime(kitsu_id: int)` that fetches anime data from the Kitsu API, creates an Anime record and one Seasons record (season 1) in a single transaction, mapping Kitsu fields per the design document | Restrictions: Do NOT add a Flask route here — this is pure business logic only. Use existing session from database.py. Handle all error cases (API unreachable, 404, malformed data) by raising descriptive exceptions. Follow existing transaction patterns from data_pull.py. Ensure the Seasons record is linked via anime_id foreign key. | _Leverage: `data_pull.py` for the Kitsu request pattern, `const.py` for API base URL and headers, `db_models/anime.py` and `db_models/seasons.py` for model constructors | _Requirements: Requirements 1.1, 1.2, 1.3, 1.4_ | Success: Function fetches anime from Kitsu, creates Anime record with correct field mapping, creates Seasons record linked to the anime, commits atomically, raises descriptive exceptions on all error paths, function signature matches spec_

- [x] 2. Create Kitsu import Flask route (`routes/kitsu.py`)
  - File: `routes/kitsu.py` (new)
  - Create Flask Blueprint with `POST /anime/kitsu-import` endpoint
  - Accept JSON body `{kitsuId: number}`, validate it's an integer
  - Call `common_funcs/kitsu.py:fetch_and_store_kitsu_anime()`
  - Return JSON responses with appropriate status codes:
    - 200: `{id, title, message}` on success
    - 400: `{message}` on invalid input or malformed data
    - 404: `{message}` on Kitsu anime not found
    - 409: `{message}` if anime already exists
    - 500: `{message}` on DB or API errors
  - Use existing patterns from `routes/anime.py` for request handling
  - Purpose: HTTP layer — handles request/response, delegates to service
  - _Leverage: `routes/anime.py` (blueprint pattern, JSON response patterns, exception handling), `project_exceptions/exceptions.py` (custom exceptions)_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_
  - _Prompt: Role: Backend Developer with expertise in Flask REST APIs | Task: Create `routes/kitsu.py` Flask Blueprint with POST /anime/kitsu-import endpoint that validates input, calls the Kitsu service, and returns appropriate JSON responses with correct status codes | Restrictions: Must validate kitsuId is a valid integer before calling the service. Return JSON error responses matching the format used in routes/anime.py. Do not add authentication — consistent with /anime/create behavior. Handle all exceptions from the service layer and map them to correct HTTP status codes. | _Leverage: `routes/anime.py` for blueprint setup, request handling, JSON response patterns | _Requirements: Requirements 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_ | Success: Endpoint accepts valid kitsuId, returns 200 on success with anime id/title, returns 400 on invalid input, 404 on not found, 409 on duplicate, 500 on errors, follows existing route patterns_

- [x] 3. Register route blueprint and add frontend page + routing
  - Files:
    - `main.py` (modify) — register `kitsu_routes` blueprint
    - `oat-frontend/src/BackendRequests/kitsu.ts` (new) — frontend API helper
    - `oat-frontend/src/Pages/KitsuImport.tsx` (new) — import page component
    - `oat-frontend/src/App.tsx` (modify) — add `/kitsu-import` route
  - **3a.** Register the blueprint in `main.py`:
    - Import `kitsu_routes` from `routes.kitsu`
    - Call `app.register_blueprint(kitsu_routes)`
  - **3b.** Create `kitsu.ts` frontend API helper:
    - Export `kitsuImport(kitsuId: number)` function using the existing `engine` from `backendRequests/base.ts`
    - Follow the same pattern as `animePost` from `backendRequests/anime.ts`
  - **3c.** Create `KitsuImport.tsx` page:
    - Input field for Kitsu Anime ID (number input)
    - Submit button
    - Loading state (disable button, show "Importing...")
    - Error message display (using MUI Typography, color error)
    - Success message display (show anime title on success)
    - Auth redirect — if user is not logged in, redirect to `/signin` (use AuthContext pattern from `AddAnime.tsx`)
    - Follow component patterns from `Pages/AddAnime.tsx` (InputComponent, SubmitBtn, etc.)
  - **3d.** Add route to `App.tsx`:
    - Add `/kitsu-import` route pointing to `KitsuImport` component
    - Follow existing route patterns in `App.tsx`
  - Purpose: Wire up the backend route and create the frontend entry point
  - _Leverage: `main.py` (blueprint registration), `routes/anime.py` (existing blueprints), `BackendRequests/anime.ts` (API helper pattern), `Pages/AddAnime.tsx` (form/UI patterns), `App.tsx` (routing patterns)_
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2_
  - _Prompt: Role: Full-stack Developer with expertise in Flask and React | Task: Register the Kitsu import blueprint in main.py, create the frontend API helper (kitsu.ts), build the KitsuImport page component with form/input/submit/error/loading states, and add the /kitsu-import route to App.tsx | Restrictions: Follow exact existing patterns — do not deviate from how blueprints are registered in main.py, do not deviate from how API helpers are structured in BackendRequests/, do not deviate from how forms are built in AddAnime.tsx, use existing MUI components and form controls. The page must redirect to /signin if user is not authenticated. | _Leverage: `main.py` for blueprint registration, `BackendRequests/anime.ts` for API helper pattern, `Pages/AddAnime.tsx` for form/UI pattern, `App.tsx` for routing | _Requirements: Requirements 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2_ | Success: Backend route registered and accessible at POST /anime/kitsu-import, frontend page renders at /kitsu-import, form works end-to-end (enter ID → submit → see success/error), loading state shown during import, unauthenticated users redirected to signin_

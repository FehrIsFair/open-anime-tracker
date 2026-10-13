# Tasks Document: List Management & Status Tabs

- [x] 1. Define ListStatus Enum
  - File: `enums/db_enums.py` (modify)
  - Define `ListStatus(enum.Enum)` with options: `plan_to_watch = 'plan_to_watch'`, `watching = 'watching'`, `complete = 'complete'`, `dropped = 'dropped'`, `on_hold = 'on_hold'`
  - Purpose: Provide domain-level status constants for user anime lists
  - _Leverage: `enums/db_enums.py`_
  - _Requirements: 1.1_
  - _Prompt: Role: Backend Python Developer | Task: Add ListStatus enum to enums/db_enums.py with plan_to_watch, watching, complete, dropped, on_hold members. Follow project conventions in .agents/rules/enums.md. | Restrictions: Keep existing enums intact. | Leverage: enums/db_enums.py | Requirements: 1.1 | Success: ListStatus enum is defined with 5 string values._

- [x] 2. Update List SQLAlchemy Model
  - File: `db_models/list.py` (modify)
  - Add `status = Column(Enum(ListStatus), nullable=False, default=ListStatus.plan_to_watch)`, `created_at`, `updated_at`, unique constraint `uq_user_anime_list` on `('user_id', 'anime_id')`, and `make_json()` method
  - Purpose: Enable status tracking, auditing, and serialization on the List model
  - _Leverage: `db_models/list.py`, `db_models/ratings.py`_
  - _Requirements: 1.2, 1.3, 1.4, 1.5_
  - _Prompt: Role: Backend Database Engineer | Task: Update db_models/list.py to include status Enum, timestamps, unique constraint on user_id + anime_id, and make_json() method. Follow conventions in .agents/rules/db_models.md. | Restrictions: Inherit from db_models.base.Base, skip _sa_instance_state in make_json. | Leverage: db_models/ratings.py | Requirements: 1.2, 1.3, 1.4, 1.5 | Success: Model contains status enum, timestamps, unique constraint, and make_json._

- [x] 3. Create Alembic Migration for List Status & Constraints
  - File: `alembic/versions/f5a6b7c8d9e0_add_status_and_timestamps_to_lists.py` (new)
  - Add migration script creating PostgreSQL enum `liststatus`, adding columns `status`, `created_at`, `updated_at`, and unique constraint `uq_user_anime_list` to `lists` table, with mirrored downgrade
  - Purpose: Apply schema changes to PostgreSQL database safely
  - _Leverage: `alembic/versions/e4f5a6b7c8d9_add_comment_to_ratings.py`, `.agents/rules/alembic.md`_
  - _Requirements: 2.1, 2.2_
  - _Prompt: Role: Database Migration Engineer | Task: Create Alembic migration script chained after e4f5a6b7c8d9. Handle PostgreSQL enum creation with postgresql.ENUM, add columns status, created_at, updated_at, and unique constraint uq_user_anime_list to lists table. Ensure downgrade cleanly drops constraint, columns, and enum. Follow .agents/rules/alembic.md. | Restrictions: Ensure create_type=False and checkfirst=True on PG enum. | Leverage: alembic/versions/e4f5a6b7c8d9_add_comment_to_ratings.py | Requirements: 2.1, 2.2 | Success: Alembic upgrade head and downgrade -1 operate cleanly._

- [x] 4. Rebuild List Routes Blueprint
  - File: `routes/list.py` (modify)
  - Replace deprecated `FlaskView` with `list_routes = Blueprint('list', __name__)`. Implement `GET /list` (with status filtering and joined anime + user rating details), `POST /list` (upsert), `PATCH /list/<anime_id>` (status update), `DELETE /list/<anime_id>` (remove), and `GET /list/anime/<anime_id>` (check status)
  - Purpose: Provide complete authenticated REST API for list operations
  - _Leverage: `routes/anime.py`, `database.py`, `common_funcs/ratings.py`_
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7_
  - _Prompt: Role: Backend Flask Engineer | Task: Modernize routes/list.py using Blueprint('list', __name__). Authenticate via sesh['username']. Implement GET /list (joining Anime and Rating models), POST /list, PATCH /list/<anime_id>, DELETE /list/<anime_id>, and GET /list/anime/<anime_id>. Validate status with get_list_status helper. Return consistent responses via make_response. Follow .agents/rules/routes.md. | Restrictions: Use shared session from database.py. Do not use FlaskView. | Leverage: routes/anime.py | Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7 | Success: All 5 endpoints function with proper status codes, auth checks, and error handling._

- [x] 5. Register List Blueprint in Flask Main App
  - File: `main.py` (modify)
  - Import `list_routes` from `routes.list` and register with `app.register_blueprint(list_routes)`
  - Purpose: Mount `/list` API endpoints on the running Flask server
  - _Leverage: `main.py`_
  - _Requirements: 3.1_
  - _Prompt: Role: Backend Flask Engineer | Task: Import list_routes from routes.list and register it with app.register_blueprint(list_routes) in main.py. | Restrictions: Keep existing blueprints registered. | Leverage: main.py | Requirements: 3.1 | Success: list_routes is registered on the app._

- [x] 6. Update Agent Rules Documentation
  - File: `.agents/rules/enums.md` and `.agents/rules/routes.md` (modify)
  - Document `ListStatus` in `enums.md` and update `routes/list.py` status from deprecated to active Blueprint in `routes.md`
  - Purpose: Keep repository architecture documentation and AI agent instructions synchronized
  - _Leverage: `.agents/rules/enums.md`, `.agents/rules/routes.md`_
  - _Requirements: 1.1, 3.1_
  - _Prompt: Role: Technical Writer | Task: Update .agents/rules/enums.md with ListStatus enum details and usage. Update .agents/rules/routes.md to document the active list blueprint endpoints and remove deprecated FlaskView notes. | Restrictions: Maintain existing rule file structure. | Leverage: .agents/rules/enums.md, .agents/rules/routes.md | Requirements: 1.1, 3.1 | Success: Documentation accurately reflects current codebase state._

- [x] 7. Add Backend Unit & Integration Tests
  - File: `tests/test_list_management.py` (new)
  - Add pytest test suite covering: List model creation & constraints, `GET /list` (filtering and joins), `POST /list` (creation & upsert), `PATCH /list/<anime_id>` status change, `DELETE /list/<anime_id>`, unauthenticated 401 response, and invalid status 400 response
  - Purpose: Ensure automated regression testing for list operations
  - _Leverage: `tests/test_rating_quarantine.py`_
  - _Requirements: 1.1, 1.4, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7_
  - _Prompt: Role: QA / Test Engineer | Task: Create comprehensive pytest suite in tests/test_list_management.py using client fixture and test user setup. Test CRUD endpoints, authentication enforcement, validation, and database state. | Restrictions: Clean up test fixtures after run. | Leverage: tests/test_rating_quarantine.py | Requirements: 1.1, 1.4, 3.1-3.7 | Success: All list tests execute and pass._

- [x] 8. Add TypeScript Models for List Management
  - File: `oat-frontend/src/Models/list.ts` (new)
  - Define `ListStatus` type, `STATUS_LABELS` map, `UserListItem` interface, and helper utilities
  - Purpose: Provide strong typing for list responses across the React frontend
  - _Leverage: `oat-frontend/src/Models/anime.ts`_
  - _Requirements: 4.2, 4.3_
  - _Prompt: Role: Frontend TypeScript Engineer | Task: Create oat-frontend/src/Models/list.ts defining ListStatus ('plan_to_watch' | 'watching' | 'complete' | 'dropped' | 'on_hold'), human-readable STATUS_LABELS dictionary, and UserListItem interface matching the backend GET /list response. | Restrictions: Follow strict TypeScript typings. | Leverage: oat-frontend/src/Models/anime.ts | Requirements: 4.2, 4.3 | Success: Types accurately model backend response._

- [x] 9. Add List API Requests Module
  - File: `oat-frontend/src/BackendRequests/list.ts` (new)
  - Implement `fetchUserList()`, `addOrUpdateAnimeInList()`, `updateAnimeStatusInList()`, `removeAnimeFromList()`, `fetchAnimeListStatus()` using shared `engine`
  - Purpose: Provide client-side API functions for list interactions
  - _Leverage: `oat-frontend/src/BackendRequests/anime.ts`, `oat-frontend/src/BackendRequests/base.ts`_
  - _Requirements: 3.2, 3.3, 3.4, 3.5_
  - _Prompt: Role: Frontend API Engineer | Task: Implement API request functions in oat-frontend/src/BackendRequests/list.ts using the base engine axios instance with withCredentials: true. | Restrictions: Proper error propagation and typing. | Leverage: oat-frontend/src/BackendRequests/anime.ts | Requirements: 3.2-3.5 | Success: API functions export typed promises._

- [x] 10. Create "My List" Page with Tabs, Sorting, and Re-Rating
  - File: `oat-frontend/src/Pages/UserList.tsx` (new)
  - Implement full list page featuring: MUI Tabs for statuses with count badges, sort dropdown (Rating, Title, Date), search filtering, anime cards with status selector, remove action, inline/dialog re-rating modal with score selector and comment blurb, empty states, and QA test IDs
  - Purpose: Main user-facing dashboard for list management
  - _Leverage: `oat-frontend/src/Pages/GetAnime.tsx`, `oat-frontend/src/Components/MechanicalRatingScroller/MechanicalPinLocRating.tsx`, `.agents/rules/frontend_testids.md`_
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 5.1, 5.2, 5.3, 5.4, 5.5_
  - _Prompt: Role: Frontend React Engineer | Task: Create oat-frontend/src/Pages/UserList.tsx. Provide tabs for All and each status with counts. Display anime cards with title link, content rating, community rating, user rating, and status dropdown. Include quick re-rate dialog/control allowing users to update their score (1-10) and comment. Include empty states per tab and sort controls. Attach strict data-testid attributes per .agents/rules/frontend_testids.md. | Restrictions: Protect with AuthContext, clean error handling. | Leverage: oat-frontend/src/Pages/GetAnime.tsx | Requirements: 4.1-4.5, 5.1-5.5 | Success: UserList renders tabs, filters by status, updates status, and re-rates smoothly._

- [x] 11. Add Navigation and Route for "My List"
  - Files: `oat-frontend/src/Header/user-nav.tsx` and `oat-frontend/src/App.tsx` (modify)
  - Add `{ path: '/my-list', text: 'My List' }` to `user-nav.tsx`, and add `<Route path='/my-list' element={<AuthRoute><UserList /></AuthRoute>} />` to `App.tsx`
  - Purpose: Enable seamless in-app navigation to the user's anime list
  - _Leverage: `oat-frontend/src/Header/user-nav.tsx`, `oat-frontend/src/App.tsx`_
  - _Requirements: 4.1_
  - _Prompt: Role: Frontend React Engineer | Task: Add My List to nav routes in oat-frontend/src/Header/user-nav.tsx and add the protected route /my-list in oat-frontend/src/App.tsx. | Restrictions: Keep existing routes working. | Leverage: oat-frontend/src/Header/user-nav.tsx, oat-frontend/src/App.tsx | Requirements: 4.1 | Success: Users can click My List in navigation and access /my-list._

- [x] 12. Add List Status Selector to Anime Details Page
  - File: `oat-frontend/src/Pages/AnimeDetails.tsx` (modify)
  - Add list status indicator and dropdown selector (e.g. "Add to List" or current status "Watching", etc.) in the Anime Details page header
  - Purpose: Allow users to add anime to their list or change status directly while exploring anime details
  - _Leverage: `oat-frontend/src/Pages/AnimeDetails.tsx`, `oat-frontend/src/BackendRequests/list.ts`_
  - _Requirements: 5.1, 5.2_
  - _Prompt: Role: Frontend React Engineer | Task: Update oat-frontend/src/Pages/AnimeDetails.tsx to fetch the user's current list status for this anime, and render a list status selector allowing users to set or change status directly. Add compliant QA test IDs. | Restrictions: Preserve existing details and rating components. | Leverage: oat-frontend/src/Pages/AnimeDetails.tsx | Requirements: 5.1, 5.2 | Success: Users can manage list status directly from Anime Details._

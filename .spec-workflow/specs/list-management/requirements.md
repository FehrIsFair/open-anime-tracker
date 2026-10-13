# Requirements Document: List Management & Status Tabs

## Introduction
This feature introduces a comprehensive anime list management system for Open Anime Tracker. Users can categorize anime titles into distinct watch statuses (`Plan to Watch`, `Watching`, `Complete`, `Dropped`, `On Hold`), view their personal anime list organized across status tabs, sort entries by ratings or titles, update statuses seamlessly, and re-rate anime directly from their list.

## Alignment with Product Vision
According to `product.md`, Open Anime Tracker aims to provide anime enthusiasts with a personal, fast, and satisfying tracking experience. Status tracking is the core backbone of any anime tracking application (comparable to MyAnimeList or AniList), allowing users to maintain their backlog, track what they are currently viewing, archive finished shows, and manage their personal ratings in one unified dashboard.

## Requirements

### Requirement 1: List Status Enum & Database Model
**User Story:** As a user, I want anime in my list to have a defined watch status (`Plan to Watch`, `Watching`, `Complete`, `Dropped`, `On Hold`) so that I can organize and filter my anime catalog.

#### Acceptance Criteria
1. WHEN a `ListStatus` enum is defined in `enums/db_enums.py` THEN it SHALL support the following values:
   - `plan_to_watch` ("Plan to Watch")
   - `watching` ("Watching")
   - `complete` ("Complete")
   - `dropped` ("Dropped")
   - `on_hold` ("On Hold")
2. WHEN an entry in the `lists` table is created or queried THEN it SHALL persist and return the `status` column using the `ListStatus` enum.
3. WHEN a user adds an anime to their list without specifying a status THEN the system SHALL default the status to `plan_to_watch`.
4. WHEN the `List` model is updated THEN it SHALL enforce a unique constraint on `('user_id', 'anime_id')` to ensure a user has at most one list record per anime.
5. WHEN the `List` model is serialized via `make_json()` THEN it SHALL return `id`, `anime_id`, `user_id`, `status`, `created_at`, and `updated_at`.

### Requirement 2: Alembic Database Migration
**User Story:** As a developer, I want an Alembic migration script that creates the PostgreSQL enum and adds `status`, timestamps, and unique constraints to the `lists` table.

#### Acceptance Criteria
1. WHEN the migration is upgraded THEN the system SHALL create the PostgreSQL enum type `liststatus` with all 5 status values and add `status`, `created_at`, `updated_at` columns and `uq_user_anime_list` unique constraint to the `lists` table.
2. WHEN the migration is downgraded THEN the system SHALL cleanly remove the unique constraint, drop the added columns, and drop the `liststatus` enum type in reverse order without errors.

### Requirement 3: List Management API (Blueprint & Routes)
**User Story:** As a frontend client, I want RESTful API endpoints under a `/list` Blueprint to fetch, add, update status, and remove anime from the current authenticated user's list.

#### Acceptance Criteria
1. WHEN `routes/list.py` is implemented THEN it SHALL use Flask `Blueprint('list', __name__)` and be registered in `main.py` (replacing the deprecated `FlaskView`).
2. WHEN an authenticated user sends `GET /list` (with optional `status` query parameter) THEN the system SHALL return list entries for that user, joined with the corresponding anime metadata (title, jp_title, type, content_rating, community rating, image/desc) and the user's personal rating (from the `Rating` model).
3. WHEN an authenticated user sends `POST /list` with `anime_id` and optional `status` THEN the system SHALL validate the status, create or update (upsert) the user's list entry, and return HTTP 200 with the saved item.
4. WHEN an authenticated user sends `PATCH /list/<anime_id>` with `status` THEN the system SHALL update the status for that anime in the user's list and return HTTP 200.
5. WHEN an authenticated user sends `DELETE /list/<anime_id>` THEN the system SHALL remove the anime from the user's list and return HTTP 200.
6. WHEN an unauthenticated request is made to any `/list` endpoint THEN the system SHALL return HTTP 401 Unauthorized.
7. WHEN an invalid status string is provided THEN the system SHALL return HTTP 400 Bad Request.

### Requirement 4: List Page UI with Status Tabs & Sorting
**User Story:** As a user, I want a dedicated "My List" page with status tabs and sorting options so that I can easily navigate and filter my tracked anime.

#### Acceptance Criteria
1. WHEN an authenticated user views the navigation bar THEN a "My List" link SHALL be visible, navigating to `/my-list`.
2. WHEN the user navigates to `/my-list` THEN the page SHALL display tabs for "All", "Watching", "Plan to Watch", "Complete", "On Hold", and "Dropped", each displaying the count of anime in that category.
3. WHEN a user selects a tab THEN only the anime matching that status SHALL be displayed (or all anime if "All" is selected).
4. WHEN the user selects a sort option ("Highest Rated", "Lowest Rated", "Title (A-Z)", "Recently Added") THEN the displayed list SHALL sort accordingly.
5. WHEN a tab has no items THEN an empty state message SHALL be displayed with a clear call-to-action to browse anime.

### Requirement 5: In-Place Status Management & Re-Rating
**User Story:** As a user, I want to change an anime's status and re-rate it directly from my list page without leaving the page.

#### Acceptance Criteria
1. WHEN viewing a list item card THEN the user SHALL see a status selector dropdown allowing them to switch the status (e.g. from "Watching" to "Complete").
2. WHEN the status is changed THEN the backend SHALL be updated and the UI (including tab counts and tab content) SHALL immediately reflect the change.
3. WHEN viewing a list item card THEN the user SHALL see their current personal rating (or "Unrated") and a "Re-rate" / rating control.
4. WHEN the user interacts with the re-rate control and submits a score THEN the rating SHALL be updated via `animeRate()` and the new score displayed immediately.
5. WHEN the user clicks "Remove" on a list item THEN the anime SHALL be removed from the list after confirmation, with the UI updated immediately.

## Non-Functional Requirements

### Code Architecture and Modularity
- Modernize `routes/list.py` to match the project's standard Blueprint pattern using `database.py`'s shared session.
- Encapsulate list API calls in `oat-frontend/src/BackendRequests/list.ts`.
- Create clean, modular TypeScript types in `oat-frontend/src/Models/list.ts`.

### Usability & Automation (QA Test IDs)
- All interactive controls, tabs, cards, and dynamic state elements MUST include `data-testid` attributes following the project's 3-segment convention (`qa-<element_name>-<action_or_data>`).

### Security
- All list endpoints must verify authentication against `session['username']` and restrict data access strictly to the logged-in user's records.

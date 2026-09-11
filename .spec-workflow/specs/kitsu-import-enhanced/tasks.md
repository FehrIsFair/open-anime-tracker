# Tasks Document

- [x] 1. Add anime search endpoint to routes/anime.py
  - File: `routes/anime.py` (modify)
  - Add `GET /anime/search?q=<query>` endpoint that queries the Anime table by title (case-insensitive LIKE match), returns up to 10 results as `{anime: [{id, title, _type, seasons, episodes, desc, status}]}`.
  - Use SQLAlchemy `func.lower` for case-insensitive matching. Only match if query is at least 2 characters.
  - Purpose: Provide backend support for the frontend anime search feature.
  - _Leverage: `routes/anime.py` existing `index()` query pattern, `database.session`
  - _Requirements: 1.1, 1.2, 1.3, 1.4

- [x] 2. Add animeSearch function to Frontend API helper
  - File: `oat-frontend/src/BackendRequests/anime.ts` (modify)
  - Add `animeSearch(query: string)` function that calls `GET /anime/search?q=<query>` using the existing `engine`. Returns `Promise<any>`.
  - Follow the same error handling pattern as the existing `animeGet` function.
  - Purpose: Frontend helper for the anime search API endpoint.
  - _Leverage: `oat-frontend/src/BackendRequests/anime.ts` existing `animeGet` function
  - _Requirements: 1.1, 1.2, 1.3, 1.4

- [x] 3. Add importSeasons function to kitsu API helper
  - File: `oat-frontend/src/BackendRequests/kitsu.ts` (modify)
  - Define a `Season` interface: `{ seasonNumber: number; kitsuId: number; typeSeason: string; hasParts: boolean; part: number | null }`.
  - Add `importSeasons(animeId: number, seasons: Season[]): Promise<any>` function that calls `POST /anime/kitsu-import-seasons` with `{ animeId, seasons }`.
  - Follow the same error handling pattern as the existing `kitsuImport` function.
  - Purpose: Frontend helper for the multi-season import API endpoint.
  - _Leverage: `oat-frontend/src/BackendRequests/kitsu.ts` existing `kitsuImport` function
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6

- [x] 4. Add import_seasons_to_anime service function
  - File: `common_funcs/kitsu.py` (modify)
  - Add `import_seasons_to_anime(anime_id: int, seasons: list[dict]) -> dict` function that:
    1. Validates the anime exists (query by ID).
    2. For each season dict, creates a `Seasons` record using `season_number`, `anime_id`, `type_season` (from the dict, default `SeasonType.SEASON`), and `part` (if provided).
    3. Uses `session.commit()` for all seasons at once.
    4. On success, returns `{id: anime.id, title: anime.title, message, seasonsCreated: len(seasons)}`.
    5. On failure, rolls back and raises `RuntimeError`.
  - Purpose: Service layer for the multi-season import, keeping it separate from the route handler.
  - _Leverage: `common_funcs/kitsu.py` existing `fetch_and_store_kitsu_anime` function (same session pattern), `db_models.seasons.Seasons` model, `db_models.anime.Anime` model, `database.session`
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5

- [x] 5. Add multi-season import endpoint to routes/kitsu.py
  - File: `routes/kitsu.py` (modify)
  - Add `POST /anime/kitsu-import-seasons` endpoint that:
    1. Parses JSON body `{animeId, seasons}`.
    2. Validates `animeId` is a positive integer and `seasons` is a non-empty list.
    3. For each season entry, validates it has `seasonNumber` (positive integer) and `kitsuId` (positive integer).
    4. Calls `import_seasons_to_anime` from the service layer with the seasons list.
    5. Returns the result on success (200), or appropriate error codes (400, 404, 500).
  - Purpose: HTTP entry point for the multi-season import feature.
  - _Leverage: `routes/kitsu.py` existing `kitsu_import` endpoint (same blueprint, validation pattern)
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6

- [x] 6. Add SeasonType enum to frontend Enums
  - File: `oat-frontend/src/Enums/AnimeType.tsx` (modify)
  - Add a `SeasonType` export alongside the existing enums: `export const SeasonTypeEnum = [{label: 'Season', value: 'season'}, {label: 'ONA', value: 'ona'}, {label: 'OVA', value: 'ova'}, {label: 'Special', value: 'special'}]`
  - Purpose: Provide the season type options for the season type dropdown in the form.
  - _Leverage: `oat-frontend/src/Enums/AnimeType.tsx` existing enum exports
  - _Requirements: 4.1, 4.2, 4.3

- [x] 7. Rewrite KitsuImport.tsx with enhanced multi-season form
  - File: `oat-frontend/src/Pages/KitsuImport.tsx` (modify)
  - Full rewrite with search → select → season builder → submit flow.
  - Purpose: The main UI for the enhanced Kitsu import feature.
  - _Leverage: All files from tasks 1-6
  - _Requirements: 1.1-1.4, 2.1-2.5, 3.1-3.5, 4.1-4.3, 6.1-6.5

- [ ] 8. Implement and test the feature end-to-end
  - File: Verify all files from tasks 1-7 are correct
  - Start Docker infrastructure (PostgreSQL + Redis).
  - Run database migrations if needed (no new models, but verify schema).
  - Start Flask backend and verify both endpoints respond.
  - Start frontend and test the full flow: search → select anime → add seasons → configure parts → submit.
  - Purpose: Validate the complete feature works correctly.
  - _Leverage: Existing project development workflow from AGENTS.md
  - _Requirements: All

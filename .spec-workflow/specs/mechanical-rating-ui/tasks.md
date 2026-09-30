# Tasks Document: Mechanical Pin Loc Rating UI & Comments

- [x] 1. Update Rating SQLAlchemy model
  - File: `db_models/ratings.py` (modify)
  - Add `comment = Column(String(500), nullable=True)`, update `__init__` and `make_json()`
  - Purpose: Persist brief blurbs with ratings
  - _Leverage: `db_models/ratings.py`_
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 2. Create Alembic migration for comment column
  - File: `alembic/versions/e4f5a6b7c8d9_add_comment_to_ratings.py` (new)
  - Add Alembic migration script to add `comment` column to `ratings` table with downgrade support
  - Purpose: Update database schema safely
  - _Leverage: `alembic/versions/70c3d7ede669_fix_rating_season_id_foreign_key_and_.py`_
  - _Requirements: 1.4_

- [x] 3. Update rating business logic for comments & reviews
  - File: `common_funcs/ratings.py` (modify)
  - Update `submit_user_rating` to handle `comment`, add `get_anime_reviews` query function
  - Purpose: Support comment upserting and community review retrieval
  - _Leverage: `common_funcs/ratings.py`_
  - _Requirements: 1.1, 1.2, 2.1, 2.3_

- [x] 4. Update anime routes for rating comments, user ratings, and reviews endpoint
  - File: `routes/anime.py` (modify)
  - Accept `comment` in `rate_anime`, inject `user_rating` in `get_anime_by_id`, add `GET /anime/<id>/reviews`
  - Purpose: Provide full API endpoints for rating and review blurbs
  - _Leverage: `routes/anime.py`_
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 5. Add backend unit & integration tests
  - File: `tests/test_ratings_comments.py` (new)
  - Add tests for rating with comment, updates, character limit validation, and reviews endpoint
  - Purpose: Automated verification of backend rating and comment behavior
  - _Leverage: `tests/test_rating_quarantine.py`_
  - _Requirements: 1.1, 1.2, 2.1, 2.2, 2.3_

- [x] 6. Update frontend models and API requests
  - File: `oat-frontend/src/BackendRequests/anime.ts` (modify)
  - Add `animeRate` and `animeGetReviews` API functions with TypeScript interfaces
  - Purpose: Enable frontend communication with rating and review endpoints
  - _Leverage: `oat-frontend/src/BackendRequests/anime.ts`_
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 7. Create Mechanical Pin Loc Rating component
  - File: `oat-frontend/src/Components/MechanicalRatingScroller/MechanicalPinLocRating.tsx` (new)
  - Implement vertical scroller (10 top, 1 bottom), click-and-drag physics, pin detents, analog readout, comment blurb field, and submit button
  - Purpose: The core tactile rating UI (visual detent feedback)
  - _Leverage: `oat-frontend/src/FormComps/TextAreaComp.tsx`_
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3_

- [x] 8. Create Community Reviews feed component
  - File: `oat-frontend/src/Components/CommunityReviews.tsx` (new)
  - Render list of user ratings, usernames, formatted timestamps, and blurbs
  - Purpose: Display other users' reviews on anime details
  - _Requirements: 5.1_

- [x] 9. Integrate Mechanical Rating UI and Community Reviews into Anime Details page
  - File: `oat-frontend/src/Pages/AnimeDetails.tsx` (modify)
  - Mount `MechanicalPinLocRating` for the show and seasons, and render `CommunityReviews`
  - Purpose: Connect tactile rating experience to the live anime details view
  - _Leverage: `oat-frontend/src/Pages/AnimeDetails.tsx`_
  - _Requirements: 4.3, 5.1_

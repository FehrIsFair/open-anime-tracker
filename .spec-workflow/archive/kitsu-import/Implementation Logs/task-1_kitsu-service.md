# Task 1 Implementation Log: Kitsu API Service

**Timestamp:** 2026-09-07  
**Task:** Create Kitsu API service (`common_funcs/kitsu.py`)  
**Status:** Completed

## Summary
Created `common_funcs/kitsu.py` with `fetch_and_store_kitsu_anime(kitsu_id: int)` function that fetches anime data from the Kitsu API, creates an Anime record and one Seasons record (season 1), and commits both in a single transaction.

## Files Modified/Created
| File | Action | Lines |
|------|--------|-------|
| `common_funcs/kitsu.py` | Created | ~120 |

## Key Implementation Details
- Custom exceptions: `KitsuAPIError` (API errors like 404), `KitsuDataError` (malformed data)
- `_fetch_kitsu_data()` — raw API fetch with error handling
- `_parse_anime_kwargs()` — maps Kitsu fields to Anime model fields (titles, description, type, rating, dates, episodes, content rating)
- `_parse_season_kwargs()` — maps Kitsu fields to Seasons model fields
- `fetch_and_store_kitsu_anime()` — orchestrates the full flow: fetch → parse → create Anime → flush → create Seasons → commit/rollback
- Uses `session.flush()` to get anime.id before committing both records atomically

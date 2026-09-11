# Requirements Document

## Introduction

This feature allows users to import anime data from the Kitsu API by entering a Kitsu anime ID. Instead of the current manual process of fetching JSON data from Kitsu and then inserting it into the database via `data_pull.py` / `data_store.py` scripts, users will have a simple web-based form to trigger the import directly from the frontend. The backend will handle the API call to Kitsu, parse the response, and store the anime in the database. The frontend will display success or error feedback.

## Alignment with Product Vision

Open Anime Tracker is a tool for managing and tracking anime ratings. This feature reduces friction for adding new anime to the database, eliminating the need to manually fetch and parse JSON files. It streamlines the data entry workflow and supports accurate, structured anime data ingestion.

## Requirements

### Requirement 1: Backend API — Import Anime by Kitsu ID

**User Story:** As a user, I want to submit a Kitsu anime ID through the web app so that the system fetches and stores the anime data automatically.

#### Acceptance Criteria

1. WHEN a POST request is sent to `/anime/kitsu-import` with a JSON body containing `kitsuId` THEN the system SHALL call the Kitsu API at `https://kitsu.io/api/edge/anime/{kitsuId}`
2. IF the Kitsu API returns a 404 or invalid response THEN the system SHALL return a `404` response with a descriptive error message
3. IF the Kitsu API returns invalid or missing data THEN the system SHALL return a `400` response with a descriptive error message
4. WHEN the anime data is successfully fetched and stored in the database THEN the system SHALL return a `200` response with the stored anime's `id`, `title`, and a success message
5. IF the database save fails THEN the system SHALL return a `500` response with a descriptive error message
6. IF the `kitsuId` is missing or not a valid integer THEN the system SHALL return a `400` response with an appropriate error

### Requirement 2: Frontend — Kitsu Import Form

**User Story:** As a user, I want a form on the frontend where I can enter a Kitsu anime ID and hit submit so that the anime is fetched and stored.

#### Acceptance Criteria

1. WHEN the user views the import page THEN they SHALL see an input field labeled "Kitsu Anime ID" and a "Import" submit button
2. WHEN the user enters a valid integer ID and clicks submit THEN the frontend SHALL send a POST request to `/anime/kitsu-import` with the ID
3. WHEN the request succeeds THEN the frontend SHALL display a success message with the stored anime title
4. WHEN the request fails THEN the frontend SHALL display the error message from the backend
5. WHEN the user leaves the field empty or enters a non-integer THEN the frontend SHALL show a client-side validation error

### Requirement 3: Frontend — Navigation & Routing

**User Story:** As a user, I want to navigate to the import page from the app so that I can access the Kitsu import feature.

#### Acceptance Criteria

1. WHEN the user navigates to `/kitsu-import` THEN the Kitsu Import page SHALL be displayed
2. WHEN the user is not logged in THEN they SHALL be redirected to `/signin`

## Non-Functional Requirements

### Code Architecture and Modularity
- **Single Responsibility Principle**: Kitsu API fetching logic should be in a dedicated service/utility file (e.g., `common_funcs/kitsu.py`)
- **Modular Design**: The route, service, and frontend component should be independently testable
- **Dependency Management**: Use existing `const.kitsu_api_base` and `const.kitsu_headers` for API configuration
- **Clear Interfaces**: The backend route should accept a clean JSON payload and return a consistent JSON response

### Performance
- The Kitsu API call should complete within 5 seconds; a timeout should be enforced
- The import operation should be synchronous (not backgrounded) given its simplicity

### Security
- Input validation on the `kitsuId` parameter to prevent injection or malformed requests
- No authentication required for the import endpoint (consistent with existing `/anime/create` behavior)

### Reliability
- Graceful error handling for all failure modes: Kitsu API unavailable, invalid ID, database errors
- Database transactions should be rolled back on failure

### Usability
- Clear success/error messages displayed in the UI
- Loading state shown during the import operation to prevent double-submits

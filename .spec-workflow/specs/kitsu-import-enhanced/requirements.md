# Requirements Document

## Introduction

Enhance the existing Kitsu import feature to support importing an anime with multiple seasons and parts. Currently, importing from Kitsu only creates a single season (season 1). Many anime are split across multiple seasons and parts (e.g., Attack on Titan Season 4 was split into Part 1, Part 2, Part 3). This enhancement allows users to specify multiple seasons, each optionally with parts, and associate them with an existing site anime (identified by site anime ID).

## Alignment with Product Vision

The Open Anime Tracker is a tool for managing anime rating data. Supporting multi-season, multi-part imports aligns with the product's goal of accurately tracking anime data. The database already supports seasons and parts — only the frontend and backend import logic need updating.

## Requirements

### Requirement 1: Site Anime Lookup with Debounced Search
**User Story:** As a user, I want to search for my site's anime by name so that I can select the correct anime to attach seasons to.

#### Acceptance Criteria
1. WHEN a user types into the search input THEN the system SHALL display a debounced (300ms) list of matching anime from the site database
2. WHEN a user selects an anime from the search results THEN the system SHALL display the selected anime title and store its ID for submission
3. WHEN the user clears the search input THEN the system SHALL clear the selected anime and hide the results list
4. WHEN no anime matches the search query THEN the system SHALL display "No anime found" in the dropdown

### Requirement 2: Dynamic Season Builder
**User Story:** As a user, I want to add multiple seasons to an anime so that I can accurately represent an anime with multiple seasons.

#### Acceptance Criteria
1. WHEN a user clicks "Add Season" THEN the system SHALL create a new season entry form
2. WHEN a user clicks "Add Season" at least once THEN at least one season entry form SHALL be visible
3. WHEN a user has two or more season entries THEN each entry SHALL have a "Remove Season" button
4. WHEN a user clicks "Remove Season" THEN that specific season entry SHALL be removed from the form
5. The minimum number of seasons submitted SHALL be one

### Requirement 3: Season Part Support
**User Story:** As a user, I want to mark a season as having parts and specify those parts so that I can accurately represent split-cour anime like Attack on Titan.

#### Acceptance Criteria
1. WHEN a user is editing a season entry THEN they SHALL see a checkbox labeled "Has Parts"
2. WHEN the "Has Parts" checkbox is checked THEN a number input for "Part Number" SHALL appear
3. WHEN the "Has Parts" checkbox is unchecked THEN the "Part Number" input SHALL be hidden and its value cleared
4. The part number input SHALL accept positive integers only
5. The part number input SHALL have a default value of 1

### Requirement 4: Season Type Selection
**User Story:** As a user, I want to specify the type of each season so that the system correctly classifies it in the database.

#### Acceptance Criteria
1. WHEN a user is editing a season entry THEN they SHALL see a dropdown for "Season Type"
2. The season type dropdown SHALL offer the options: Season, ONA, OVA, Special
3. The default season type SHALL be "Season"

### Requirement 5: Kitsu ID Input
**User Story:** As a user, I want to enter the Kitsu ID for each season so that the system can identify which season from Kitsu corresponds to this entry.

#### Acceptance Criteria
1. WHEN a user is editing a season entry THEN they SHALL see a number input labeled "Kitsu ID"
2. The Kitsu ID input SHALL accept positive integers only
3. The Kitsu ID input SHALL be required (non-empty)
4. The Kitsu ID is stored on the backend but NOT displayed on the Seasons model (it is metadata only)

### Requirement 5: Backend API for Multi-Season Import
**User Story:** As a user, when I submit the multi-season import form, the system SHALL create the anime and all associated seasons (with optional parts) in the database.

#### Acceptance Criteria
1. WHEN a user submits the form with a valid site anime ID and one or more seasons THEN the system SHALL create all seasons for that anime
2. WHEN a season entry includes a part number THEN the season record SHALL include that part value
3. WHEN a season entry does not include a part number THEN the season record's part field SHALL be null
4. WHEN any database operation fails THEN the system SHALL rollback all changes and return an error
5. WHEN the site anime ID does not exist THEN the system SHALL return a 404 error
6. WHEN no seasons are provided THEN the system SHALL return a 400 error

### Requirement 6: Form Submission and Validation
**User Story:** As a user, I want clear validation feedback when submitting the form so that I can fix errors before submission.

#### Acceptance Criteria
1. WHEN the form is submitted without a selected site anime THEN the system SHALL display "Please select an anime from the search results."
2. WHEN the form is submitted with no seasons THEN the system SHALL display "At least one season is required."
3. WHEN a season has a part number but "Has Parts" is not checked THEN the system SHALL NOT include that part in the submission
4. WHEN the submission succeeds THEN the system SHALL display a success message with the anime title and the number of seasons created
5. WHEN the submission fails due to a server error THEN the system SHALL display a generic error message

### Requirement 7: Non-Functional Requirements

#### Performance
- The anime search debounce SHALL be 300ms to balance responsiveness with API load
- The search API SHALL return results within 500ms for typical databases

#### Reliability
- All database operations for a single submission SHALL be atomic (all-or-nothing)
- The frontend SHALL handle network errors gracefully with user-friendly messages

#### Usability
- The form SHALL be intuitive: search anime → add seasons → configure each season → submit
- Season entries SHALL be clearly separated visually (e.g., cards or bordered sections)

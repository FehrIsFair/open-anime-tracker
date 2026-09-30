# Requirements Document: Mechanical Pin Loc Rating UI & Comments

## Introduction
This feature introduces a tactile, mechanical "pin loc" vertical scroller rating interface for Open Anime Tracker, accompanied by a brief comment/blurb field. It allows users to rate anime shows and individual seasons with an intuitive, physics-driven slider while sharing qualitative impressions.

## Alignment with Product Vision
In accordance with the product vision in `product.md`, Open Anime Tracker aims to provide anime enthusiasts with a delightful, responsive, and personal tracking experience. The mechanical rating interaction elevates a standard form input into an engaging, tactile experience, while comments foster deeper community discussion.

## Requirements

### Requirement 1: Rating Database Model with Comment Support
**User Story:** As a user, I want my rating record to store an optional commentary blurb so that I can capture my thoughts alongside my numerical score.
#### Acceptance Criteria
1. WHEN a rating is submitted with a comment string THEN the system SHALL persist the comment (up to 500 characters) in the `ratings` table.
2. WHEN a rating is submitted without a comment THEN the system SHALL store `NULL` or preserve the existing comment appropriately.
3. WHEN a rating with comment is requested via API THEN the system SHALL return the `comment` attribute in the JSON representation.
4. WHEN an Alembic migration is executed THEN the `comment` column SHALL be added without dropping or corrupting existing ratings data.

### Requirement 2: Rating Submission & Retrieval API
**User Story:** As a frontend client, I want API endpoints to submit scores with comments and retrieve user-specific ratings as well as community reviews.
#### Acceptance Criteria
1. WHEN a POST request is made to `/anime/<anime_id>/rate` with `rating`, optional `comment`, and optional `season_id` THEN the system SHALL validate the rating (1-10) and comment length (<= 500 chars) and persist the record.
2. WHEN an authenticated user requests `/anime/<anime_id>` THEN the response SHALL include the user's personal rating and comment under `user_rating` for the show and for any rated seasons.
3. WHEN a GET request is made to `/anime/<anime_id>/reviews` THEN the system SHALL return recent community reviews including score, comment blurb, username, and timestamp.

### Requirement 3: Mechanical Pin Loc Vertical Scroller Component
**User Story:** As a user, I want to click, hold, and drag a vertical mechanical pin slider between 1 and 10 with tactile detents and sound effects so that rating feels mechanical and satisfying.
#### Acceptance Criteria
1. WHEN the user views the rating component THEN it SHALL display a vertical scale from 10 (at the top) to 1 (at the bottom) with mechanical detent notches.
2. WHEN the user clicks and drags the pin up or down THEN the pin SHALL track mouse movement and snap smoothly to discrete integer detents from 1 to 10.
3. WHEN the pin clicks into a new detent THEN a subtle mechanical audio click SHALL play via Web Audio API (unless muted).
4. WHEN the user toggles the sound button THEN the mechanical audio clicks SHALL be muted or unmuted.
5. WHEN the rating changes THEN an analog readout display SHALL reflect the current score and qualitative label.

### Requirement 4: Comment Blurb Input & Submission
**User Story:** As a user, I want a text field to write a brief blurb and lock in my rating.
#### Acceptance Criteria
1. WHEN the user types into the blurb field THEN a character counter SHALL display the remaining length out of 500 characters.
2. WHEN the user clicks "Lock In Rating" THEN the rating and blurb SHALL be submitted via API with visual loading and success confirmation.
3. WHEN an existing rating is loaded THEN the scroller and blurb field SHALL initialize with the user's previously saved values.

### Requirement 5: Community Reviews Feed
**User Story:** As a user, I want to see what other people thought of the anime and seasons so that I can read community impressions.
#### Acceptance Criteria
1. WHEN viewing the Anime Details page THEN a community reviews section SHALL display other users' scores, usernames, dates, and comment blurbs.

## Non-Functional Requirements
### Code Architecture and Modularity
- Follow Flask blueprint architecture in `routes/anime.py` and service functions in `common_funcs/ratings.py`.
- Encapsulate the scroller in a modular, reusable React component in `oat-frontend/src/Components/MechanicalRatingScroller/`.
### Performance
- Web Audio API click synthesis should run on an existing AudioContext without memory leaks or audio glitches.
- Pointer drag tracking should use efficient requestAnimationFrame or standard pointer capture.
### Usability & Accessibility
- Keyboard arrow navigation and direct click-to-notch support in addition to dragging.

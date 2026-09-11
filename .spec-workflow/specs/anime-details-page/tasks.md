# Tasks Document

- [x] 1. Add backend endpoint to fetch anime by ID with seasons
  - File: `routes/anime.py` (modify)
  - Add a new route `@anime_routes.route('/anime/<int:anime_id>', methods=['GET'])` that queries an anime by ID, loads its associated seasons via a SQLAlchemy join on `seasons.anime_id == anime.id`, and returns a JSON response containing both the anime data (`anime.make_json()`) and a list of season data (each season serialized as a dict with id, season_number, title, episodes, desc, rating, air_date, end_date, type_season, part).
  - Return 404 with `{'message': 'Anime not found'}` when anime doesn't exist.
  - Return 500 on SQLAlchemyError.
  - Purpose: Provides the backend API endpoint that the frontend will call to fetch anime details with its seasons.
  - _Leverage: `routes/anime.py` existing routes pattern, `db_models/anime.py` Anime model, `db_models/seasons.py` Seasons model
  - _Requirements: 4.1, 4.2, 4.3
  - _Prompt: Role: Backend developer with expertise in Flask and SQLAlchemy | Task: Add a new GET route to the anime_routes blueprint in routes/anime.py. The route should be `/anime/<int:anime_id>` and accept an integer anime_id as a path parameter. Inside the handler: 1) Query the database for an Anime where Anime.id == anime_id. 2) If not found, return make_response({'message': 'Anime not found'}, 404). 3) If found, query Seasons where Seasons.anime_id == anime_id. 4) Build a response dict with keys 'anime' (set to anime.make_json()) and 'seasons' (set to a list of dicts, each containing: id, season_number, title, episodes, desc, rating, air_date, end_date, type_season, part — use the season's __dict__ but exclude _sa_instance_state). 5) Return make_response(response_dict, 200). 6) Wrap in try/except for SQLAlchemyError, returning 500 on error. Follow the exact pattern used by existing routes in this file (imports, make_response, try/except). | Restrictions: Do not modify existing routes. Only add the new route. Use SQLAlchemy session from the existing import. | _Leverage: routes/anime.py, db_models/anime.py, db_models/seasons.py | _Requirements: 4.1, 4.2, 4.3 | Success: The new route returns correct JSON with anime and seasons data, returns 404 for missing anime, and handles DB errors gracefully.

- [x] 2. Add TypeScript interfaces for season and anime details response
  - File: `oat-frontend/src/Models/season.ts` (new)
  - Create a new TypeScript file with:
    - `Season` interface with fields: `id: number`, `season_number: number`, `title: string | null`, `episodes: number | null`, `desc: string | null`, `rating: number | null`, `air_date: string | null`, `end_date: string | null`, `type_season: string`, `part: number | null`
  - Purpose: Define the TypeScript type for season data returned from the backend.
  - _Leverage: `oat-frontend/src/Models/anime.ts` for TypeScript interface patterns
  - _Requirements: 3.1
  - _Prompt: Role: Frontend developer with expertise in TypeScript | Task: Create a new file at oat-frontend/src/Models/season.ts. Define and export a TypeScript interface called `Season` with the following fields (all nullable except id and season_number): title: string \| null, episodes: number \| null, desc: string \| null, rating: number \| null, air_date: string \| null, end_date: string \| null, type_season: string, part: number \| null. Also include id: number and season_number: number (non-nullable). Use the same style and formatting as the existing Anime interface in oat-frontend/src/Models/anime.ts. | Restrictions: Only create this one file. Do not modify any other files. | _Leverage: oat-frontend/src/Models/anime.ts | _Requirements: 3.1 | Success: The Season interface is defined with all required fields and is properly exported.

- [x] 3. Add frontend API function to fetch anime details with seasons
  - File: `oat-frontend/src/BackendRequests/anime.ts` (modify)
  - Add a new exported function `animeGetByIdWithSeasons(id: number)` that makes a GET request to `/anime/${id}` and returns the response data. Follow the existing pattern used by `animeGet` and `animeSearch` functions.
  - Purpose: Provides the frontend API client function for the new backend endpoint.
  - _Leverage: `oat-frontend/src/BackendRequests/anime.ts` existing `animeGet` function
  - _Requirements: 1.3, 3.1
  - _Prompt: Role: Frontend developer with expertise in TypeScript and Axios | Task: Add a new function to the existing oat-frontend/src/BackendRequests/anime.ts file. The function should be: `export const animeGetByIdWithSeasons = async (id: number) => { const res = await engine.get(\`/anime/\${id}\`); return res.data; }`. Place it after the existing `animeSearch` function. Follow the exact pattern used by `animeGet` (lines 15-18) — same structure, just different endpoint. No error handling needed at this layer (let the component handle errors). | Restrictions: Only add this one function. Do not modify existing functions. Keep the existing imports. | _Leverage: oat-frontend/src/BackendRequests/anime.ts (existing animeGet function) | _Requirements: 1.3, 3.1 | Success: The new function is added to the file, properly typed, and follows the existing pattern.

- [x] 4. Create the AnimeDetails page component
  - File: `oat-frontend/src/Pages/AnimeDetails.tsx` (new)
  - Create a new page component that:
    - Uses `useParams` from react-router-dom to get the `id` from the URL
    - Uses `Navigate` to redirect to `/signin` if the user is not logged in (same pattern as GetAnime)
    - Fetches anime details using `animeGetByIdWithSeasons` from the API
    - Displays an error state with the error message if the fetch fails
    - Displays a "Anime not found" message if the response indicates the anime doesn't exist
    - Displays the anime info section first (above seasons):
      - Title as h1, using the `h1` style from text_config
      - Rating (with "Community Rating" label, showing "No rating" if null)
      - Type, Content Rating, Japanese Title, Description
    - Then displays the seasons section below:
      - "Seasons" heading as h2, using the `h2` style from text_config
      - If no seasons: "No seasons available" message
      - For each season: a Card component (same style as GetAnime) showing season title/number, episodes, description, rating, air date, end date, and type
  - Uses Material-UI components: Box, Card, Typography, CardContent (same as GetAnime)
  - Uses the `h1`, `h2` style exports from `text_config.ts`
  - Purpose: The main page component that displays anime details and seasons.
  - _Leverage: `oat-frontend/src/Pages/GetAnime.tsx` for auth guard, loading/error patterns, card styling
  - _Requirements: 1.1, 1.2, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4
  - _Prompt: Role: Frontend developer with expertise in React, TypeScript, and Material-UI | Task: Create a new page component at oat-frontend/src/Pages/AnimeDetails.tsx. Follow the GetAnime.tsx pattern for: auth guard using useContext(AuthContext) + Navigate to /signin, loading/error state management, and Box/Card/Typography styling.

    The component should:
    1. Import and use useParams from react-router-dom to get the id
    2. Define interfaces for the response data (use inline or import Season from Models/season.ts)
    3. Use useEffect to call animeGetByIdWithSeasons(id) on mount
    4. Handle loading state with <Typography>Loading...</Typography>
    5. Handle error state with <Typography color="error">{error}</Typography>
    6. Handle 404 response by showing <Typography>Anime not found.</Typography>
    7. For successful data, render:
       - A Box wrapper with maxWidth: 800, mx: 'auto', mt: 4, p: 2
       - Anime info section first (above seasons):
         - Typography variant="h1" with h1 style for the anime title
         - Typography for rating (show "No rating" if null)
         - Typography for type, content rating, jp_title, description
       - Then seasons section:
         - Typography variant="h2" with h2 style for "Seasons" heading
         - If seasons array is empty: <Typography>No seasons available.</Typography>
         - Map over seasons: each season gets a <Card sx={{ p: 2, mb: 2 }}> with:
           - Typography variant="h4" for season title (or "Season {season_number}" if title is null/empty)
           - Typography for episodes, description, rating (show "No rating" if null), air_date, end_date, type_season
    
    Use the same Card sx={{ p: 2, mb: 2 }} style as GetAnime.tsx line 54. Import h1 and h2 from text_config. | Restrictions: Only create this one file. Do not modify any other files. Use the same styling patterns as GetAnime.tsx. | _Leverage: oat-frontend/src/Pages/GetAnime.tsx (auth, loading, error patterns), oat-frontend/src/TextFormating/text_config.ts (h1, h2 styles) | _Requirements: 1.1, 1.2, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4 | Success: The AnimeDetails component renders correctly, handles all states (loading, error, 404, no seasons), displays anime info above seasons, and uses consistent styling with the rest of the app.

- [x] 5. Add route in App.tsx and update GetAnime to link titles
  - File: `oat-frontend/src/App.tsx` (modify)
  - Add a new route: `<Route path='/anime/:id/details' element={<AuthRoute><AnimeDetails /></AuthRoute>} />` placed after the `/get-anime` route. Import `AnimeDetails` from the new page.
  - File: `oat-frontend/src/Pages/GetAnime.tsx` (modify)
  - Wrap the title Typography with a `<Link to={...}>` from react-router-dom that navigates to `/anime/{id}/details`. Add `id` to the `AnimeItem` interface.
  - Purpose: Wire up navigation from the anime title on GetAnime to the new AnimeDetails page.
  - _Leverage: `oat-frontend/src/App.tsx` existing route patterns, `react-router-dom` Link component
  - _Requirements: 1.1, 1.2
  - _Prompt: Role: Frontend developer with expertise in React and TypeScript | Task: Make two changes:

    1. In oat-frontend/src/App.tsx:
       - Add import: `import AnimeDetails from './Pages/AnimeDetails';`
       - Add a new route after the `/get-anime` route: `<Route path='/anime/:id/details' element={<AuthRoute><AnimeDetails /></AuthRoute>} />`

    2. In oat-frontend/src/Pages/GetAnime.tsx:
       - Add `id: number;` to the AnimeItem interface
       - Import Link from 'react-router-dom'
       - Wrap the `<Typography variant="h4">{item.title}</Typography>` with: `<Link to={`/anime/${item.id}/details`} style={{ textDecoration: 'none', color: 'inherit' }}>...</Link>`
       - The title should be clickable and styled to look like a link

    Follow the existing patterns in both files exactly. Keep imports organized. | Restrictions: Only modify these two files. Do not change any other routes or components. | _Leverage: oat-frontend/src/App.tsx (existing route patterns), react-router-dom Link | _Requirements: 1.1, 1.2 | Success: Clicking an anime title navigates to the correct details route, and the AnimeDetails page renders with the correct anime data.

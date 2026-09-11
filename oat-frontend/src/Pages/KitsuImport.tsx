import React, { useContext, useState, useCallback, useRef, type FormEvent } from "react";
import {
  Box,
  Typography,
  Paper,
  Divider,
  Stack,
  Tab,
  Tabs,
} from "@mui/material";
import { Navigate } from "react-router-dom";

import { h1 } from "../TextFormating/text_config";
import NumberInputComponent from "../FormComps/NumberInput";
import SubmitBtn from "../FormComps/Buttons/SubmitBtn";
import CheckBoxComponent from "../FormComps/CheckBoxComp";
import SelectComponent from "../FormComps/SelectComp";
import { SeasonTypeEnum } from "../Enums/AnimeType";
import { animeSearch } from "../BackendRequests/anime";
import { kitsuImport } from "../BackendRequests/kitsu";
import { importSeasons, type Season } from "../BackendRequests/kitsu";
import { AuthContext } from "../context/auth_context";

// ─── Single-Season Import Component ────────────────────────────────────────

const SingleSeasonImport = () => {
  const [kitsuId, setKitsuId] = useState(0);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);
  const { user } = useContext(AuthContext);

  const handleSubmit = async () => {
    setError("");
    setSuccess("");

    if (kitsuId <= 0) {
      setError("Please enter a valid Kitsu anime ID.");
      return;
    }

    setLoading(true);
    try {
      const result = await kitsuImport(kitsuId);
      setSuccess(result.message || `Anime "${result.title}" imported successfully`);
      setKitsuId(0);
    } catch (err: any) {
      const msg = err.response?.data?.message || "Failed to import anime from Kitsu.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  if (user == null) {
    return <Navigate to="/signin" />;
  }

  return (
    <Box sx={{ maxWidth: 600, mx: "auto", mt: 4, p: 2 }}>
      <Typography variant="h1" sx={h1}>
        Import from Kitsu
      </Typography>
      <Typography variant="body1" sx={{ mb: 2 }}>
        Enter a Kitsu anime ID to fetch and store it in the database.
      </Typography>
      <NumberInputComponent
        id="kitsu-id"
        label="Kitsu Anime ID"
        value={kitsuId}
        onChange={setKitsuId}
      />
      {error && (
        <Typography color="error" sx={{ mt: 1, fontSize: "0.875rem" }}>
          {error}
        </Typography>
      )}
      {success && (
        <Typography color="success.main" sx={{ mt: 1, fontSize: "0.875rem" }}>
          {success}
        </Typography>
      )}
      <SubmitBtn
        variant="contained"
        onSubmit={handleSubmit}
        disabled={loading}
        sx={{ mt: 2 }}
      >
        {loading ? "Importing..." : "Import"}
      </SubmitBtn>
    </Box>
  );
};

// ─── Multi-Season Import Component ─────────────────────────────────────────

interface AnimeSearchResult {
  id: number;
  title: string;
  _type: string;
  seasons: number;
  episodes: number;
  desc: string;
  status: string;
}

interface SeasonEntry {
  seasonNumber: number;
  kitsuId: number;
  typeSeason: string;
  hasParts: boolean;
  part: number | null;
}

const emptySeason = (startNumber: number = 2): SeasonEntry => ({
  seasonNumber: startNumber,
  kitsuId: 0,
  typeSeason: "season",
  hasParts: false,
  part: 1,
});

const MultiSeasonImport = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<AnimeSearchResult[]>([]);
  const [selectedAnime, setSelectedAnime] = useState<AnimeSearchResult | null>(null);
  const [seasons, setSeasons] = useState<SeasonEntry[]>([emptySeason(2)]);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [searchLoading, setSearchLoading] = useState(false);
  const [loading, setLoading] = useState(false);
  const { user } = useContext(AuthContext);

  // Debounced search
  const searchTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const performSearch = useCallback(async (query: string) => {
    if (query.length < 2) {
      setSearchResults([]);
      return;
    }
    setSearchLoading(true);
    try {
      const data = await animeSearch(query);
      setSearchResults(data.anime || []);
    } catch {
      setSearchResults([]);
    } finally {
      setSearchLoading(false);
    }
  }, []);

  const handleSearchChange = (value: string) => {
    setSearchQuery(value);
    setSelectedAnime(null);
    setSearchResults([]);

    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }
    searchTimeoutRef.current = setTimeout(() => {
      performSearch(value);
    }, 300);
  };

  // Cleanup timeout on unmount
  React.useEffect(() => {
    return () => {
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current);
      }
    };
  }, []);

  const selectAnime = (anime: AnimeSearchResult) => {
    setSelectedAnime(anime);
    setSearchQuery(anime.title);
    setSearchResults([]);
  };

  const addSeason = () => {
    setSeasons([
      ...seasons,
      { ...emptySeason(seasons.length + 2) },
    ]);
  };

  const removeSeason = (index: number) => {
    if (seasons.length <= 1) return;
    setSeasons(seasons.filter((_, i) => i !== index).map((s, i) => ({
      ...s,
      seasonNumber: i + 1,
    })));
  };

  const updateSeason = (index: number, field: keyof SeasonEntry, value: any) => {
    setSeasons(
      seasons.map((s, i) => (i === index ? { ...s, [field]: value } : s))
    );
  };

  const handleSubmit = async () => {
    setError("");
    setSuccess("");

    if (!selectedAnime) {
      setError("Please select an anime from the search results.");
      return;
    }

    if (seasons.length < 1) {
      setError("At least one season is required.");
      return;
    }

    for (const s of seasons) {
      if (s.kitsuId <= 0) {
        setError(`Season ${s.seasonNumber} requires a Kitsu ID.`);
        return;
      }
    }

    setLoading(true);
    try {
      const result = await importSeasons(selectedAnime.id, seasons);
      setSuccess(
        result.message ||
          `Anime "${result.title}" imported with ${result.seasonsCreated} season(s).`
      );
      setSeasons([emptySeason()]);
      setSelectedAnime(null);
      setSearchQuery("");
    } catch (err: any) {
      const msg = err.response?.data?.message || "Failed to import seasons.";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  if (user == null) {
    return <Navigate to="/signin" />;
  }

  return (
    <Box sx={{ maxWidth: 700, mx: "auto", mt: 4, p: 2 }}>
      <Typography variant="h1" sx={h1}>
        Import Seasons from Kitsu
      </Typography>
      <Typography variant="body1" sx={{ mb: 2 }}>
        Search for your site anime, then add seasons 2+ with their Kitsu IDs. Season 1 is already imported via the Single Season import.
      </Typography>

      <form onSubmit={handleSubmit}>
        {/* Anime Search */}
        <Stack spacing={1} sx={{ mb: 3 }}>
          <Typography variant="subtitle2">Search Anime</Typography>
          <input
            type="text"
            placeholder="Type to search anime..."
            value={searchQuery}
            onChange={(e) => handleSearchChange(e.target.value)}
            style={{
              padding: "10px 12px",
              fontSize: "1rem",
              border: "1px solid",
              borderColor: searchResults.length > 0 && !selectedAnime ? "error.main" : "divider",
              borderRadius: 4,
              width: "100%",
              boxSizing: "border-box",
            }}
          />
          {searchLoading && (
            <Typography variant="caption" color="text.secondary">
              Searching...
            </Typography>
          )}
          {searchResults.length > 0 && !selectedAnime && (
            <Paper variant="outlined" sx={{ maxHeight: 200, overflow: "auto" }}>
              {searchResults.map((anime) => (
                <Box
                  key={anime.id}
                  role="option"
                  sx={{
                    px: 2,
                    py: 1,
                    cursor: "pointer",
                    "&:hover": { backgroundColor: "action.hover" },
                  }}
                  onClick={() => selectAnime(anime)}
                >
                  <Typography variant="body2">{anime.title}</Typography>
                  <Typography variant="caption" color="text.secondary">
                    Type: {anime._type}
                  </Typography>
                </Box>
              ))}
            </Paper>
          )}
          {selectedAnime && (
            <Paper variant="outlined" sx={{ p: 1, backgroundColor: "success.light" }}>
              <Typography variant="body2" color="success.dark">
                ✓ Selected: {selectedAnime.title}
              </Typography>
            </Paper>
          )}
          {!searchLoading && searchQuery.length >= 2 && searchResults.length === 0 && !selectedAnime && (
            <Typography variant="caption" color="error">
              No anime found.
            </Typography>
          )}
        </Stack>

        <Divider sx={{ my: 2 }} />

        {/* Season Entries */}
        {seasons.map((season, index) => (
          <Paper key={index} variant="outlined" sx={{ p: 2, mb: 2 }}>
            <Stack spacing={2}>
              <Typography variant="h5" sx={{ mb: 0 }}>
                Season {season.seasonNumber}
              </Typography>

              <NumberInputComponent
                id={`season-${index}-kitsu-id`}
                label="Kitsu ID"
                value={season.kitsuId}
                onChange={(v) => updateSeason(index, "kitsuId", v)}
              />

              <SelectComponent
                id={`season-${index}-type`}
                label="Season Type"
                value={season.typeSeason}
                onChange={(v) => updateSeason(index, "typeSeason", v)}
                options={SeasonTypeEnum}
              />

              <CheckBoxComponent
                label="Has Parts"
                value={season.hasParts}
                onChange={(v) => updateSeason(index, "hasParts", v)}
              />

              {season.hasParts && (
                <NumberInputComponent
                  id={`season-${index}-part`}
                  label="Part Number"
                  value={season.part ?? 1}
                  onChange={(v) => updateSeason(index, "part", v)}
                />
              )}

              {seasons.length >= 2 && (
                <Box sx={{ textAlign: "right" }}>
                  <button
                    type="button"
                    onClick={() => removeSeason(index)}
                    style={{
                      color: "error.main",
                      background: "none",
                      border: "1px solid error.main",
                      borderRadius: 4,
                      padding: "4px 12px",
                      cursor: "pointer",
                      fontSize: "0.875rem",
                    }}
                  >
                    Remove Season
                  </button>
                </Box>
              )}
            </Stack>
          </Paper>
        ))}

        {/* Add Season Button */}
        <Box sx={{ textAlign: "center", mb: 2 }}>
          <button
            type="button"
            onClick={addSeason}
            style={{
              padding: "8px 20px",
              fontSize: "0.875rem",
              border: "1px dashed",
              borderRadius: 4,
              cursor: "pointer",
              color: "text.primary",
              borderColor: "divider",
              background: "transparent",
            }}
          >
            + Add Season
          </button>
        </Box>

        <Divider sx={{ my: 2 }} />

        {/* Submit */}
        <SubmitBtn
          variant="contained"
          onSubmit={handleSubmit}
          disabled={loading}
          fullWidth
          sx={{ mt: 2, py: 1.5 }}
        >
          {loading ? "Importing..." : "Import Seasons"}
        </SubmitBtn>

        {error && (
          <Typography color="error" sx={{ mt: 1, fontSize: "0.875rem" }}>
            {error}
          </Typography>
        )}
        {success && (
          <Typography color="success.main" sx={{ mt: 1, fontSize: "0.875rem" }}>
            {success}
          </Typography>
        )}
      </form>
    </Box>
  );
};

// ─── Main Page ─────────────────────────────────────────────────────────────

const KitsuImport = () => {
  const [tab, setTab] = useState(0);

  return (
    <Box>
      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: "divider", maxWidth: 700, mx: "auto" }}>
        <Tabs value={tab} onChange={(_, v) => setTab(v)}>
          <Tab label="Single Season" />
          <Tab label="Multi Season" />
        </Tabs>
      </Box>

      {tab === 0 && <SingleSeasonImport />}
      {tab === 1 && <MultiSeasonImport />}
    </Box>
  );
};

export default KitsuImport;

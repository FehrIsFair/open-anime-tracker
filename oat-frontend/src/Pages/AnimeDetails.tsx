import React, { useContext } from "react";
import { Box, Card, Typography } from "@mui/material";
import { Navigate, useParams } from "react-router-dom";

import { h1, h2 } from "../TextFormating/text_config";
import { AuthContext } from "../context/auth_context";
import { animeGetByIdWithSeasons } from "../BackendRequests/anime";
import { Season } from "../Models/season";

interface AnimeData {
  id: number;
  title: string;
  desc: string;
  content_rating: string;
  jp_title: string;
  _type: string;
  rating: number | null;
}

const AnimeDetails = () => {
  const [anime, setAnime] = React.useState<AnimeData | null>(null);
  const [seasons, setSeasons] = React.useState<Season[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState("");
  const { user } = useContext(AuthContext);
  const { id } = useParams<{ id: string }>();

  React.useEffect(() => {
    const loadAnimeDetails = async () => {
      if (!id) return;
      try {
        const data = await animeGetByIdWithSeasons(Number(id));
        if (data.anime) {
          setAnime(data.anime);
          setSeasons(data.seasons || []);
        }
      } catch (err: any) {
        const status = err.response?.status;
        if (status === 404) {
          setError("not_found");
        } else {
          setError(err.response?.data?.message || "Failed to load anime details.");
        }
      } finally {
        setLoading(false);
      }
    };

    loadAnimeDetails();
  }, [id]);

  if (user == null) {
    return <Navigate to="/signin" />;
  }

  if (loading) {
    return <Typography>Loading...</Typography>;
  }

  if (error === "not_found") {
    return <Typography>Anime not found.</Typography>;
  }

  if (error) {
    return <Typography color="error">{error}</Typography>;
  }

  if (!anime) {
    return null;
  }

  return (
    <Box sx={{ maxWidth: 800, mx: "auto", mt: 4, p: 2 }}>
      {/* Anime Info Section */}
      <Typography variant="h1" sx={h1}>
        {anime.title}
      </Typography>
      <Typography>Community Rating: {anime.rating ?? "No rating"}</Typography>
      <Typography>Type: {anime._type}</Typography>
      <Typography>Content Rating: {anime.content_rating}</Typography>
      {anime.jp_title && <Typography>JP Title: {anime.jp_title}</Typography>}
      {anime.desc && <Typography>{anime.desc}</Typography>}

      {/* Seasons Section */}
      <Typography variant="h2" sx={{ ...h2, mt: 3 }}>
        Seasons
      </Typography>
      {seasons.length === 0 && (
        <Typography>No seasons available.</Typography>
      )}
      {seasons.map((season, idx) => (
        <Card key={season.id ?? idx} sx={{ p: 2, mb: 2 }}>
          <Typography variant="h4">
            {season.title || `Season ${season.season_number}`}
          </Typography>
          <Typography>Season Number: {season.season_number}</Typography>
          <Typography>Type: {season.type_season}</Typography>
          {season.episodes && <Typography>Episodes: {season.episodes}</Typography>}
          {season.desc && <Typography>{season.desc}</Typography>}
          <Typography>
            Rating: {season.rating ?? "No rating"}
          </Typography>
          {season.air_date && <Typography>Air Date: {season.air_date}</Typography>}
          {season.end_date && (
            <Typography>End Date: {season.end_date}</Typography>
          )}
        </Card>
      ))}
    </Box>
  );
};

export default AnimeDetails;

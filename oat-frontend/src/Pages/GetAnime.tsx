import React, { useContext } from "react";
import { Box, Card, Typography } from "@mui/material";
import { Link, Navigate } from "react-router-dom";

import { h1 } from "../TextFormating/text_config";
import { AuthContext } from "../context/auth_context";
import { animeGet } from "../BackendRequests/anime";

interface AnimeItem {
  id: number;
  title: string;
  desc: string;
  content_rating: string;
  jp_title: string;
  _type: string;
  rating: number | null;
}

const GetAnime = () => {
  const [animeList, setAnimeList] = React.useState<AnimeItem[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState("");
  const { user } = useContext(AuthContext);

  React.useEffect(() => {
    const loadAnime = async () => {
      try {
        const data = await animeGet();
        setAnimeList(data.data || data);
      } catch (err: any) {
        setError(err.response?.data?.message || "Failed to load anime.");
      } finally {
        setLoading(false);
      }
    };

    loadAnime();
  }, []);

  if (user == null) {
    return <Navigate to="/signin" />;
  }

  return (
    <Box sx={{ maxWidth: 800, mx: "auto", mt: 4, p: 2 }}>
      <Typography variant="h1" sx={h1}>
        Your Anime
      </Typography>
      {loading && <Typography>Loading...</Typography>}
      {error && <Typography color="error">{error}</Typography>}
      {!loading && !error && animeList.length === 0 && (
        <Typography>No anime entries yet.</Typography>
      )}
      {animeList.map((item, idx) => (
        <Card key={idx} sx={{ p: 2, mb: 2 }}>
          <Link to={`/anime/${item.id}/details`} style={{ textDecoration: 'none', color: 'inherit' }}>
            <Typography variant="h4">{item.title}</Typography>
          </Link>
          <Typography>{item.desc}</Typography>
          <Typography>Content Rating: {item.content_rating}</Typography>
          <Typography>JP Title: {item.jp_title}</Typography>
          <Typography>Type: {item._type}</Typography>
          <Typography>Community Rating: {item.rating}</Typography>
        </Card>
      ))}
    </Box>
  );
};
export default GetAnime;

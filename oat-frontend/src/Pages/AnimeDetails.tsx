import React, { useContext, useState } from "react";
import {
  Box,
  Card,
  Typography,
  Divider,
  Button,
  Collapse,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
} from "@mui/material";
import StarBorderIcon from '@mui/icons-material/StarBorder';
import { Navigate, useParams } from "react-router-dom";

import { h1, h2 } from "../TextFormating/text_config";
import { AuthContext } from "../context/auth_context";
import { animeGetByIdWithSeasons } from "../BackendRequests/anime";
import {
  fetchAnimeListStatus,
  addToList,
  removeFromList,
} from "../BackendRequests/list";
import { ListStatus, STATUS_LABELS } from "../Models/list";
import { Season } from "../Models/season";
import { UserRatingRecord } from "../Models/anime";
import MechanicalPinLocRating from "../Components/MechanicalRatingScroller/MechanicalPinLocRating";
import CommunityReviews from "../Components/CommunityReviews";

interface AnimeData {
  id: number;
  title: string;
  desc: string;
  content_rating: string;
  jp_title: string;
  _type: string;
  rating: number | null;
  user_rating?: UserRatingRecord | null;
}

const AnimeDetails = () => {
  const [anime, setAnime] = React.useState<AnimeData | null>(null);
  const [seasons, setSeasons] = React.useState<Season[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState("");
  const [reviewsTrigger, setReviewsTrigger] = useState<number>(0);
  const [expandedSeasonRatingId, setExpandedSeasonRatingId] = useState<number | null>(null);
  const [listStatus, setListStatus] = useState<ListStatus | 'none'>('none');
  const [listStatusUpdating, setListStatusUpdating] = useState<boolean>(false);
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

    const loadListStatus = async () => {
      if (!id) return;
      try {
        const res = await fetchAnimeListStatus(Number(id));
        if (res.in_list && res.status) {
          setListStatus(res.status);
        } else {
          setListStatus('none');
        }
      } catch (err) {
        console.error('Failed to load list status:', err);
      }
    };

    loadAnimeDetails();
    loadListStatus();
  }, [id]);

  const handleListStatusChange = async (newVal: string) => {
    if (!id) return;
    setListStatusUpdating(true);
    try {
      if (newVal === 'none') {
        await removeFromList(Number(id));
        setListStatus('none');
      } else {
        await addToList(Number(id), newVal as ListStatus);
        setListStatus(newVal as ListStatus);
      }
    } catch (err) {
      console.error('Failed to update list status:', err);
    } finally {
      setListStatusUpdating(false);
    }
  };

  if (user == null) {
    return <Navigate to="/signin" />;
  }

  if (loading) {
    return <Typography data-testid="qa-anime_details_loading-loading">Loading...</Typography>;
  }

  if (error === "not_found") {
    return <Typography data-testid="qa-anime_details_not_found-empty">Anime not found.</Typography>;
  }

  if (error) {
    return <Typography color="error" data-testid="qa-anime_details_error-error">{error}</Typography>;
  }

  if (!anime) {
    return null;
  }

  return (
    <Box sx={{ maxWidth: 840, mx: "auto", mt: 4, p: 2 }}>
      {/* Anime Info Section */}
      <Typography variant="h1" sx={h1}>
        {anime.title}
      </Typography>

      {/* Watch Status Selector */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, my: 2 }}>
        <FormControl size="small" sx={{ minWidth: 180 }}>
          <InputLabel id="anime-details-list-status-label">Watch Status</InputLabel>
          <Select
            labelId="anime-details-list-status-label"
            id="anime-details-list-status"
            value={listStatus}
            label="Watch Status"
            onChange={(e) => handleListStatusChange(e.target.value)}
            disabled={listStatusUpdating}
            data-testid="qa-anime_details_list_status-select"
          >
            <MenuItem value="none"><em>Not in list</em></MenuItem>
            <MenuItem value="watching">Watching</MenuItem>
            <MenuItem value="plan_to_watch">Plan to Watch</MenuItem>
            <MenuItem value="complete">Complete</MenuItem>
            <MenuItem value="on_hold">On Hold</MenuItem>
            <MenuItem value="dropped">Dropped</MenuItem>
          </Select>
        </FormControl>
        {listStatus !== 'none' && (
          <Chip
            label={STATUS_LABELS[listStatus]}
            color={listStatus === 'complete' ? 'success' : listStatus === 'watching' ? 'primary' : 'default'}
            size="small"
            data-testid="qa-anime_details_list_status-data"
          />
        )}
      </Box>

      <Typography data-testid="qa-anime_community_rating-data">Community Rating: {anime.rating ?? "No rating"}</Typography>
      <Typography data-testid="qa-anime_type-data">Type: {anime._type}</Typography>
      <Typography data-testid="qa-anime_content_rating-data">Content Rating: {anime.content_rating}</Typography>
      {anime.jp_title && <Typography data-testid="qa-anime_jp_title-data">JP Title: {anime.jp_title}</Typography>}
      {anime.desc && <Typography sx={{ mt: 1 }} data-testid="qa-anime_desc-data">{anime.desc}</Typography>}


      {/* Show Level Mechanical Pin Loc Rating */}
      <Box sx={{ mt: 3, mb: 3 }}>
        <MechanicalPinLocRating
          animeId={anime.id}
          initialRating={anime.user_rating?.rating ?? null}
          initialComment={anime.user_rating?.comment ?? ''}
          onRatingSubmitted={(newRating, newComment) => {
            setAnime((prev) =>
              prev
                ? {
                    ...prev,
                    user_rating: {
                      id: prev.user_rating?.id ?? 0,
                      user_id: prev.user_rating?.user_id ?? 0,
                      rating: newRating,
                      comment: newComment || null,
                      anime_id: anime.id,
                      season_id: null,
                    },
                  }
                : null
            );
            setReviewsTrigger((prev) => prev + 1);
          }}
        />
      </Box>

      {/* Seasons Section */}
      <Typography variant="h2" sx={{ ...h2, mt: 4 }}>
        Seasons
      </Typography>
      {seasons.length === 0 && (
        <Typography data-testid="qa-anime_seasons_empty-empty">No seasons available.</Typography>
      )}
      {seasons.map((season, idx) => {
        const isSeasonRatingOpen = expandedSeasonRatingId === season.id;
        const seasonTitle = season.title || `Season ${season.season_number}`;

        return (
          <Card key={season.id ?? idx} sx={{ p: 2.5, mb: 2.5, background: '#181b22', border: '1px solid #28303d' }} data-testid="qa-season_card-card">
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <Box>
                <Typography variant="h4" sx={{ color: '#f1f5f9', fontWeight: 700 }} data-testid="qa-season_title-data">
                  {seasonTitle}
                </Typography>
                <Typography variant="body2" sx={{ color: '#94a3b8' }} data-testid="qa-season_details-data">
                  Season Number: {season.season_number} • Type: {season.type_season}
                  {season.episodes ? ` • ${season.episodes} episodes` : ''}
                </Typography>
              </Box>
              <Button
                data-testid="qa-season_rate_btn-click"
                size="small"
                variant={season.user_rating ? 'contained' : 'outlined'}
                startIcon={<StarBorderIcon />}
                onClick={() =>
                  setExpandedSeasonRatingId(isSeasonRatingOpen ? null : season.id)
                }
                sx={{
                  textTransform: 'none',
                  fontSize: '0.8rem',
                  borderColor: '#38bdf8',
                  color: season.user_rating ? '#ffffff' : '#38bdf8',
                  backgroundColor: season.user_rating ? '#0284c7' : 'transparent',
                  '&:hover': {
                    backgroundColor: season.user_rating ? '#0369a1' : 'rgba(56,189,248,0.1)',
                  },
                }}
              >
                {season.user_rating
                  ? `Your Rating: ${season.user_rating.rating}/10`
                  : 'Rate Season'}
              </Button>
            </Box>

            {season.desc && <Typography sx={{ mt: 1.5, color: '#cbd5e1' }} data-testid="qa-season_desc-data">{season.desc}</Typography>}
            <Typography variant="body2" sx={{ mt: 1, color: '#94a3b8' }} data-testid="qa-season_rating-data">
              Community Rating: {season.rating ?? "No rating"}
            </Typography>
            {season.air_date && <Typography variant="caption" sx={{ display: 'block', color: '#64748b' }} data-testid="qa-season_air_date-data">Air Date: {season.air_date}</Typography>}
            {season.end_date && (
              <Typography variant="caption" sx={{ display: 'block', color: '#64748b' }} data-testid="qa-season_end_date-data">End Date: {season.end_date}</Typography>
            )}

            {/* Collapsible Season Mechanical Pin Loc Rating */}
            <Collapse in={isSeasonRatingOpen} timeout="auto" unmountOnExit>
              <Box sx={{ mt: 2.5, pt: 2, borderTop: '1px solid #28303d' }}>
                <MechanicalPinLocRating
                  animeId={anime.id}
                  seasonId={season.id}
                  seasonTitle={seasonTitle}
                  initialRating={season.user_rating?.rating ?? null}
                  initialComment={season.user_rating?.comment ?? ''}
                  compact={true}
                  onRatingSubmitted={(newRating, newComment) => {
                    setSeasons((prev) =>
                      prev.map((s) =>
                        s.id === season.id
                          ? {
                              ...s,
                              user_rating: {
                                id: s.user_rating?.id ?? 0,
                                user_id: s.user_rating?.user_id ?? 0,
                                rating: newRating,
                                comment: newComment || null,
                                anime_id: anime.id,
                                season_id: season.id,
                              },
                            }
                          : s
                      )
                    );
                    setReviewsTrigger((prev) => prev + 1);
                  }}
                />
              </Box>
            </Collapse>
          </Card>
        );
      })}

      <Divider sx={{ my: 4, borderColor: '#334155' }} />

      {/* Community Reviews Feed */}
      <CommunityReviews animeId={anime.id} refreshTrigger={reviewsTrigger} />
    </Box>
  );
}

export default AnimeDetails;


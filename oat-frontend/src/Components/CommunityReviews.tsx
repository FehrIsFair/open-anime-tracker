import React, { useEffect, useState, useCallback } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Avatar,
  Chip,
  CircularProgress,
  Divider,
} from '@mui/material';
import RateReviewIcon from '@mui/icons-material/RateReview';
import { animeGetReviews } from '../BackendRequests/anime';
import { ReviewItem } from '../Models/anime';

interface CommunityReviewsProps {
  animeId: number;
  seasonId?: number | null;
  refreshTrigger?: number;
}

export const CommunityReviews: React.FC<CommunityReviewsProps> = ({
  animeId,
  seasonId = null,
  refreshTrigger = 0,
}) => {
  const [reviews, setReviews] = useState<ReviewItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchReviews = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await animeGetReviews(animeId, seasonId);
      if (data && data.reviews) {
        setReviews(data.reviews);
      }
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to load community reviews.');
    } finally {
      setLoading(false);
    }
  }, [animeId, seasonId]);

  useEffect(() => {
    fetchReviews();
  }, [fetchReviews, refreshTrigger]);

  const getScoreColor = (score: number) => {
    if (score >= 8) return '#10b981';
    if (score >= 5) return '#f59e0b';
    return '#ef4444';
  };

  return (
    <Box sx={{ mt: 4 }} data-testid="qa-community_reviews-list">
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
        <RateReviewIcon sx={{ color: '#38bdf8' }} />
        <Typography variant="h5" sx={{ fontWeight: 700, color: '#f8fafc' }}>
          Community Reviews &amp; Blurbs
        </Typography>
        {reviews.length > 0 && (
          <Chip
            label={`${reviews.length} ${reviews.length === 1 ? 'review' : 'reviews'}`}
            size="small"
            data-testid="qa-community_reviews_count-data"
            sx={{
              backgroundColor: '#1e293b',
              color: '#94a3b8',
              fontWeight: 600,
              fontSize: '0.75rem',
            }}
          />
        )}
      </Box>

      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }} data-testid="qa-community_reviews_loading-loading">
          <CircularProgress size={28} sx={{ color: '#38bdf8' }} />
        </Box>
      )}

      {error && (
        <Typography color="error" variant="body2" data-testid="qa-community_reviews_error-error">
          {error}
        </Typography>
      )}

      {!loading && !error && reviews.length === 0 && (
        <Card
          data-testid="qa-community_reviews_empty-empty"
          sx={{
            background: '#13171f',
            border: '1px dashed #334155',
            borderRadius: 2,
            p: 3,
            textAlign: 'center',
          }}
        >
          <Typography sx={{ color: '#64748b', fontSize: '0.9rem' }}>
            No community blurbs yet. Be the first to rate and share your thoughts!
          </Typography>
        </Card>
      )}

      {!loading && reviews.length > 0 && (
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {reviews.map((review) => {
            const scoreColor = getScoreColor(review.rating);
            const dateStr = review.created_at
              ? new Date(review.created_at).toLocaleDateString(undefined, {
                  year: 'numeric',
                  month: 'short',
                  day: 'numeric',
                })
              : null;

            return (
              <Card
                key={review.id}
                data-testid="qa-review_card-card"
                sx={{
                  background: 'linear-gradient(145deg, #181c24 0%, #11141a 100%)',
                  border: '1px solid #28303d',
                  borderRadius: 2,
                  boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
                }}
              >
                <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                  <Box
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      mb: 1.5,
                    }}
                  >
                    {/* User Info */}
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.2 }}>
                      <Avatar
                        sx={{
                          width: 32,
                          height: 32,
                          fontSize: '0.85rem',
                          fontWeight: 700,
                          backgroundColor: '#334155',
                          color: '#e2e8f0',
                        }}
                      >
                        {review.username.charAt(0).toUpperCase()}
                      </Avatar>
                      <Box>
                        <Typography
                          variant="subtitle2"
                          data-testid="qa-review_username-data"
                          sx={{ fontWeight: 700, color: '#f1f5f9', lineHeight: 1.2 }}
                        >
                          {review.username}
                        </Typography>
                        {dateStr && (
                          <Typography variant="caption" sx={{ color: '#64748b' }}>
                            {dateStr}
                          </Typography>
                        )}
                      </Box>
                    </Box>

                    {/* Rating Badge */}
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      {review.season_title && (
                        <Chip
                          label={review.season_title}
                          size="small"
                          sx={{
                            backgroundColor: '#1e293b',
                            color: '#94a3b8',
                            fontSize: '0.72rem',
                          }}
                        />
                      )}
                      <Box
                        sx={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: 0.5,
                          px: 1.2,
                          py: 0.3,
                          borderRadius: 1,
                          backgroundColor: 'rgba(0,0,0,0.5)',
                          border: `1px solid ${scoreColor}`,
                          boxShadow: `0 0 8px ${scoreColor}33`,
                        }}
                      >
                        <Typography
                          data-testid="qa-review_score-data"
                          sx={{
                            fontFamily: 'monospace',
                            fontWeight: 800,
                            fontSize: '0.95rem',
                            color: scoreColor,
                          }}
                        >
                          {review.rating}
                        </Typography>
                        <Typography variant="caption" sx={{ color: '#64748b', fontWeight: 600 }}>
                          / 10
                        </Typography>
                      </Box>
                    </Box>
                  </Box>

                  {/* Comment Blurb */}
                  {review.comment ? (
                    <>
                      <Divider sx={{ my: 1, borderColor: '#232a35' }} />
                      <Typography
                        variant="body2"
                        data-testid="qa-review_comment-data"
                        sx={{
                          color: '#cbd5e1',
                          lineHeight: 1.5,
                          whiteSpace: 'pre-line',
                          fontStyle: 'italic',
                        }}
                      >
                        &ldquo;{review.comment}&rdquo;
                      </Typography>
                    </>
                  ) : (
                    <Typography
                      variant="caption"
                      sx={{ color: '#64748b', fontStyle: 'italic' }}
                    >
                      (Rated without a comment blurb)
                    </Typography>
                  )}
                </CardContent>
              </Card>
            );
          })}
        </Box>
      )}
    </Box>
  );
};

export default CommunityReviews;

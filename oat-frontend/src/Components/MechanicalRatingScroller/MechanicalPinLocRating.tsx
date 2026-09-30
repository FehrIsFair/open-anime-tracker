import React, { useState, useRef, useEffect, useCallback } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  CircularProgress,
  Alert,
  Tooltip,
} from '@mui/material';
import LockIcon from '@mui/icons-material/Lock';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import { animeRate } from '../../BackendRequests/anime';

interface MechanicalPinLocRatingProps {
  animeId: number;
  seasonId?: number | null;
  seasonTitle?: string;
  initialRating?: number | null;
  initialComment?: string | null;
  onRatingSubmitted?: (rating: number, comment?: string) => void;
  compact?: boolean;
}

const RATING_DESCRIPTIONS: Record<number, string> = {
  10: 'Masterpiece',
  9: 'Incredible',
  8: 'Great',
  7: 'Good',
  6: 'Fine',
  5: 'Average',
  4: 'Bad',
  3: 'Very Bad',
  2: 'Horrible',
  1: 'Unwatchable',
};

const RATING_STEPS = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1];

export const MechanicalPinLocRating: React.FC<MechanicalPinLocRatingProps> = ({
  animeId,
  seasonId = null,
  seasonTitle,
  initialRating = null,
  initialComment = '',
  onRatingSubmitted,
  compact = false,
}) => {
  const [selectedRating, setSelectedRating] = useState<number>(initialRating ?? 8);
  const [comment, setComment] = useState<string>(initialComment || '');
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const trackRef = useRef<HTMLDivElement | null>(null);

  // Sync initial props if they load asynchronously
  useEffect(() => {
    if (initialRating != null) {
      setSelectedRating(initialRating);
    }
    if (initialComment != null) {
      setComment(initialComment);
    }
  }, [initialRating, initialComment]);

  // Calculate rating (10 at top to 1 at bottom) from pointer Y coordinate
  const calculateRatingFromPointer = useCallback((clientY: number) => {
    if (!trackRef.current) return;
    const rect = trackRef.current.getBoundingClientRect();
    const trackHeight = rect.height;
    const clampedY = Math.max(0, Math.min(trackHeight, clientY - rect.top));
    const ratio = clampedY / trackHeight;
    // ratio = 0 is top (10), ratio = 1 is bottom (1)
    const rawVal = 10 - ratio * 9;
    const snapped = Math.round(rawVal);
    const clampedScore = Math.max(1, Math.min(10, snapped));
    setSelectedRating(clampedScore);
  }, []);

  const handlePointerDown = (e: React.PointerEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (!trackRef.current) return;
    trackRef.current.setPointerCapture(e.pointerId);
    setIsDragging(true);
    calculateRatingFromPointer(e.clientY);
  };

  const handlePointerMove = (e: React.PointerEvent<HTMLDivElement>) => {
    if (!isDragging) return;
    calculateRatingFromPointer(e.clientY);
  };

  const handlePointerUp = (e: React.PointerEvent<HTMLDivElement>) => {
    if (!isDragging) return;
    setIsDragging(false);
    try {
      if (trackRef.current?.hasPointerCapture(e.pointerId)) {
        trackRef.current.releasePointerCapture(e.pointerId);
      }
    } catch {
      // Ignore if pointer capture was already released
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowUp' || e.key === 'ArrowRight') {
      e.preventDefault();
      setSelectedRating((prev) => Math.min(10, prev + 1));
    } else if (e.key === 'ArrowDown' || e.key === 'ArrowLeft') {
      e.preventDefault();
      setSelectedRating((prev) => Math.max(1, prev - 1));
    }
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    setErrorMsg(null);
    setSuccessMsg(null);
    try {
      await animeRate(animeId, selectedRating, comment.trim() || undefined, seasonId);
      setSuccessMsg('Rating locked in!');
      if (onRatingSubmitted) {
        onRatingSubmitted(selectedRating, comment.trim());
      }
      setTimeout(() => setSuccessMsg(null), 3500);
    } catch (err: any) {
      setErrorMsg(err.response?.data?.message || 'Failed to submit rating. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  // Pin position percentage from top (10 is 0%, 1 is 100%)
  const pinPercentTop = ((10 - selectedRating) / 9) * 100;

  const trackHeightPx = compact ? 220 : 300;

  return (
    <Box
      sx={{
        background: 'linear-gradient(145deg, #1e2229 0%, #15181d 100%)',
        border: '2px solid #2e3440',
        borderRadius: 2,
        boxShadow: 'inset 0 1px 1px rgba(255,255,255,0.08), 0 8px 24px rgba(0,0,0,0.5)',
        p: compact ? 2 : 2.5,
        mb: 3,
        color: '#e2e8f0',
        position: 'relative',
        userSelect: 'none',
      }}
    >
      {/* Console Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <LockIcon sx={{ fontSize: 18, color: '#f59e0b' }} />
          <Typography
            variant="subtitle2"
            sx={{
              fontWeight: 700,
              letterSpacing: '0.12em',
              textTransform: 'uppercase',
              color: '#94a3b8',
              fontSize: '0.78rem',
            }}
          >
            {seasonTitle ? `Rate ${seasonTitle}` : 'Rate This Show'}
          </Typography>
        </Box>
        {/* Analog Digital Readout */}
        <Box
          sx={{
            background: '#090b0e',
            border: '1px solid #334155',
            borderRadius: 1,
            px: 1.5,
            py: 0.4,
            display: 'flex',
            alignItems: 'baseline',
            gap: 0.8,
            boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.8)',
          }}
        >
          <Typography
            data-testid="qa-rating_score-data"
            sx={{
              fontFamily: 'monospace',
              fontSize: '1.25rem',
              fontWeight: 800,
              color: selectedRating >= 8 ? '#10b981' : selectedRating >= 5 ? '#f59e0b' : '#ef4444',
              textShadow: '0 0 8px currentColor',
            }}
          >
            {selectedRating < 10 ? `0${selectedRating}` : selectedRating}
          </Typography>
          <Typography
            variant="caption"
            sx={{
              color: '#64748b',
              fontWeight: 600,
              letterSpacing: '0.05em',
            }}
          >
            / 10 • {RATING_DESCRIPTIONS[selectedRating]}
          </Typography>
        </Box>
      </Box>

      {/* Main Scroller & Input Row */}
      <Box sx={{ display: 'flex', gap: compact ? 2 : 3, alignItems: 'center' }}>
        {/* Mechanical Pin Loc Vertical Scroller */}
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'row',
            alignItems: 'center',
            position: 'relative',
            px: 1,
            py: 1,
            background: '#111419',
            border: '1px solid #232934',
            borderRadius: 1.5,
            boxShadow: 'inset 0 3px 8px rgba(0,0,0,0.7)',
          }}
        >
          {/* Numbers & Tick Marks Column */}
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              height: trackHeightPx,
              pr: 1.5,
              py: '4px',
            }}
          >
            {RATING_STEPS.map((num) => {
              const isSelected = selectedRating === num;
              return (
                <Box
                  key={num}
                  data-testid="qa-rating_pin-click"
                  onClick={() => setSelectedRating(num)}
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 0.6,
                    cursor: 'pointer',
                  }}
                >
                  <Typography
                    sx={{
                      fontFamily: 'monospace',
                      fontSize: '0.78rem',
                      fontWeight: isSelected ? 800 : 500,
                      color: isSelected ? '#38bdf8' : '#64748b',
                      minWidth: 18,
                      textAlign: 'right',
                      transition: 'color 0.15s ease',
                      textShadow: isSelected ? '0 0 6px rgba(56,189,248,0.7)' : 'none',
                    }}
                  >
                    {num}
                  </Typography>
                  <Box
                    sx={{
                      width: isSelected ? 10 : 6,
                      height: 2,
                      backgroundColor: isSelected ? '#38bdf8' : '#334155',
                      transition: 'all 0.15s ease',
                    }}
                  />
                </Box>
              );
            })}
          </Box>

          {/* Vertical Slot Track + Detent Pins */}
          <Box
            ref={trackRef}
            tabIndex={0}
            onPointerDown={handlePointerDown}
            onPointerMove={handlePointerMove}
            onPointerUp={handlePointerUp}
            onKeyDown={handleKeyDown}
            role="slider"
            aria-valuemin={1}
            aria-valuemax={10}
            aria-valuenow={selectedRating}
            aria-label="Mechanical Pin Loc Rating"
            data-testid="qa-rating_track-data"
            sx={{
              position: 'relative',
              width: 32,
              height: trackHeightPx,
              cursor: isDragging ? 'grabbing' : 'grab',
              outline: 'none',
              touchAction: 'none',
              '&:focus-visible': {
                outline: '2px solid #38bdf8',
                borderRadius: 1,
              },
            }}
          >
            {/* The Recessed Vertical Slot Track */}
            <Box
              sx={{
                position: 'absolute',
                left: '50%',
                top: 0,
                bottom: 0,
                width: 8,
                transform: 'translateX(-50%)',
                background: '#07090b',
                borderRadius: 4,
                boxShadow: 'inset 0 2px 6px rgba(0,0,0,0.9), 0 1px 0 rgba(255,255,255,0.06)',
                border: '1px solid #1c222b',
              }}
            />

            {/* Recessed Detent Pinholes */}
            {RATING_STEPS.map((num) => {
              const notchTopPercent = ((10 - num) / 9) * 100;
              const isLocked = selectedRating === num;
              return (
                <Box
                  key={num}
                  sx={{
                    position: 'absolute',
                    top: `calc(${notchTopPercent}% - 3px)`,
                    left: '50%',
                    transform: 'translateX(-50%)',
                    width: 6,
                    height: 6,
                    borderRadius: '50%',
                    backgroundColor: isLocked ? '#f59e0b' : '#14181f',
                    border: isLocked ? '1px solid #fbbf24' : '1px solid #2a3340',
                    boxShadow: isLocked
                      ? '0 0 8px #f59e0b, inset 0 1px 2px rgba(0,0,0,0.8)'
                      : 'inset 0 1px 2px rgba(0,0,0,0.8)',
                    transition: 'all 0.15s ease',
                    pointerEvents: 'none',
                  }}
                />
              );
            })}

            {/* Draggable Mechanical Pin Thumb */}
            <Box
              sx={{
                position: 'absolute',
                top: `calc(${pinPercentTop}% - 12px)`,
                left: '50%',
                transform: 'translateX(-50%)',
                width: 28,
                height: 24,
                borderRadius: '4px',
                background: isDragging
                  ? 'linear-gradient(180deg, #475569 0%, #1e293b 100%)'
                  : 'linear-gradient(180deg, #334155 0%, #0f172a 100%)',
                border: '2px solid #64748b',
                boxShadow: isDragging
                  ? '0 6px 14px rgba(0,0,0,0.8), 0 0 10px rgba(56,189,248,0.5), inset 0 1px 1px rgba(255,255,255,0.4)'
                  : '0 4px 8px rgba(0,0,0,0.7), inset 0 1px 1px rgba(255,255,255,0.3)',
                transition: isDragging ? 'none' : 'top 0.12s cubic-bezier(0.34, 1.56, 0.64, 1)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                pointerEvents: 'none',
              }}
            >
              {/* Mechanical Indicator Pin Line */}
              <Box
                sx={{
                  width: 14,
                  height: 3,
                  backgroundColor: '#38bdf8',
                  borderRadius: 1,
                  boxShadow: '0 0 6px #38bdf8',
                }}
              />
            </Box>
          </Box>
        </Box>

        {/* Right Section: Comment Blurb & Action Controls */}
        <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 1.5 }}>
          <Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
              <Typography variant="caption" sx={{ color: '#94a3b8', fontWeight: 600 }}>
                Thoughts / Review Blurb
              </Typography>
              <Typography
                variant="caption"
                sx={{
                  fontFamily: 'monospace',
                  color: comment.length > 450 ? '#ef4444' : '#64748b',
                }}
              >
                {comment.length} / 500
              </Typography>
            </Box>
            <TextField
              multiline
              rows={compact ? 4 : 6}
              value={comment}
              onChange={(e) => {
                if (e.target.value.length <= 500) {
                  setComment(e.target.value);
                }
              }}
              placeholder="What did you think of the animation, story, or pacing? (Brief blurb)"
              variant="outlined"
              fullWidth
              size="small"
              data-testid="qa-rating_comment-input"
              inputProps={{ 'data-testid': 'qa-rating_comment-input' }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  backgroundColor: '#0c0e12',
                  color: '#e2e8f0',
                  fontSize: '0.88rem',
                  borderRadius: 1.5,
                  border: '1px solid #232934',
                  boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.6)',
                  '&:hover': {
                    borderColor: '#475569',
                  },
                  '&.Mui-focused': {
                    borderColor: '#38bdf8',
                    boxShadow: '0 0 0 1px #38bdf8, inset 0 2px 4px rgba(0,0,0,0.6)',
                  },
                },
              }}
            />
          </Box>

          {/* Feedback Alerts */}
          {errorMsg && (
            <Alert severity="error" sx={{ py: 0.5, px: 1, fontSize: '0.8rem' }} data-testid="qa-rating_error-error">
              {errorMsg}
            </Alert>
          )}
          {successMsg && (
            <Alert
              icon={<CheckCircleOutlineIcon fontSize="inherit" />}
              severity="success"
              sx={{ py: 0.5, px: 1, fontSize: '0.8rem' }}
              data-testid="qa-rating_success-status"
            >
              {successMsg}
            </Alert>
          )}

          {/* Submit Button */}
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 'auto' }}>
            <Tooltip title="Submit score and save commentary">
              <span>
                <Button
                  data-testid="qa-rating_lock_btn-submit"
                  variant="contained"
                  onClick={handleSubmit}
                  disabled={submitting}
                  startIcon={
                    submitting ? (
                      <CircularProgress size={16} color="inherit" />
                    ) : (
                      <LockIcon sx={{ fontSize: 16 }} />
                    )
                  }
                  sx={{
                    background: 'linear-gradient(180deg, #2563eb 0%, #1d4ed8 100%)',
                    color: '#ffffff',
                    fontWeight: 700,
                    fontSize: '0.82rem',
                    textTransform: 'none',
                    letterSpacing: '0.04em',
                    px: 2.5,
                    py: 0.8,
                    borderRadius: 1.5,
                    border: '1px solid #3b82f6',
                    boxShadow: '0 4px 10px rgba(37,99,235,0.4), inset 0 1px 0 rgba(255,255,255,0.2)',
                    '&:hover': {
                      background: 'linear-gradient(180deg, #1d4ed8 0%, #1e40af 100%)',
                      boxShadow: '0 6px 14px rgba(37,99,235,0.5)',
                    },
                    '&:disabled': {
                      background: '#1e293b',
                      color: '#64748b',
                      borderColor: '#334155',
                    },
                  }}
                >
                  {submitting ? 'Locking In...' : 'Lock In Rating'}
                </Button>
              </span>
            </Tooltip>
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default MechanicalPinLocRating;

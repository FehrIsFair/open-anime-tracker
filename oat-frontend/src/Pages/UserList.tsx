import React, { useContext, useEffect, useState, useMemo } from 'react';
import {
  Box,
  Card,
  Typography,
  Tabs,
  Tab,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Alert,
  Chip,
  CircularProgress,
  Stack,
  Divider,
} from '@mui/material';
import StarIcon from '@mui/icons-material/Star';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';
import EditIcon from '@mui/icons-material/Edit';
import { Link, Navigate } from 'react-router-dom';

import { h1, h2, p } from '../TextFormating/text_config';
import { AuthContext } from '../context/auth_context';
import {
  fetchUserList,
  updateListStatus,
  removeFromList,
} from '../BackendRequests/list';
import { animeRate } from '../BackendRequests/anime';
import { ListStatus, STATUS_LABELS, UserListItem } from '../Models/list';

const TAB_STATUSES: { key: string; label: string; status?: ListStatus }[] = [
  { key: 'all', label: 'All' },
  { key: 'watching', label: 'Watching', status: 'watching' },
  { key: 'plan_to_watch', label: 'Plan to Watch', status: 'plan_to_watch' },
  { key: 'complete', label: 'Complete', status: 'complete' },
  { key: 'on_hold', label: 'On Hold', status: 'on_hold' },
  { key: 'dropped', label: 'Dropped', status: 'dropped' },
];

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

const UserList = () => {
  const { user } = useContext(AuthContext);
  const [items, setItems] = useState<UserListItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Filter & Sort State
  const [activeTab, setActiveTab] = useState<string>('all');
  const [sortBy, setSortBy] = useState<string>('updated_desc');
  const [searchQuery, setSearchQuery] = useState<string>('');

  // Re-rate Modal State
  const [reRateItem, setReRateItem] = useState<UserListItem | null>(null);
  const [ratingScore, setRatingScore] = useState<number>(8);
  const [ratingComment, setRatingComment] = useState<string>('');
  const [savingRating, setSavingRating] = useState<boolean>(false);
  const [ratingModalError, setRatingModalError] = useState<string | null>(null);

  // Load items
  const loadList = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await fetchUserList(undefined, sortBy);
      setItems(res.data || []);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to load your list.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadList();
  }, [sortBy]);

  // Counts for each status tab
  const statusCounts = useMemo(() => {
    const counts: Record<string, number> = { all: items.length };
    TAB_STATUSES.forEach((tab) => {
      if (tab.status) {
        counts[tab.key] = items.filter((i) => i.status === tab.status).length;
      }
    });
    return counts;
  }, [items]);

  // Filtered items based on active tab and search query
  const filteredItems = useMemo(() => {
    let result = [...items];

    if (activeTab !== 'all') {
      const selectedStatus = TAB_STATUSES.find((t) => t.key === activeTab)?.status;
      if (selectedStatus) {
        result = result.filter((i) => i.status === selectedStatus);
      }
    }

    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase().trim();
      result = result.filter(
        (i) =>
          i.anime.title.toLowerCase().includes(q) ||
          (i.anime.jp_title && i.anime.jp_title.toLowerCase().includes(q))
      );
    }

    return result;
  }, [items, activeTab, searchQuery]);

  // Handle status change
  const handleStatusChange = async (animeId: number, newStatus: ListStatus) => {
    try {
      await updateListStatus(animeId, newStatus);
      setItems((prev) =>
        prev.map((i) =>
          i.anime_id === animeId
            ? { ...i, status: newStatus, updated_at: new Date().toISOString() }
            : i
        )
      );
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to update status.');
    }
  };

  // Handle remove anime
  const handleRemove = async (animeId: number) => {
    try {
      await removeFromList(animeId);
      setItems((prev) => prev.filter((i) => i.anime_id !== animeId));
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to remove anime from list.');
    }
  };

  // Open Re-rate Modal
  const openReRateModal = (item: UserListItem) => {
    setReRateItem(item);
    setRatingScore(item.user_rating?.rating ?? 8);
    setRatingComment(item.user_rating?.comment ?? '');
    setRatingModalError(null);
  };

  // Submit Re-rate
  const handleSaveRating = async () => {
    if (!reRateItem) return;
    setSavingRating(true);
    setRatingModalError(null);
    try {
      await animeRate(
        reRateItem.anime_id,
        ratingScore,
        ratingComment.trim() || undefined
      );

      // Update local state
      setItems((prev) =>
        prev.map((i) =>
          i.anime_id === reRateItem.anime_id
            ? {
                ...i,
                user_rating: {
                  id: i.user_rating?.id ?? 0,
                  rating: ratingScore,
                  comment: ratingComment.trim() || null,
                },
              }
            : i
        )
      );
      setReRateItem(null);
    } catch (err: any) {
      setRatingModalError(
        err.response?.data?.message || 'Failed to save rating. Please try again.'
      );
    } finally {
      setSavingRating(false);
    }
  };

  if (!user) {
    return <Navigate to="/signin" />;
  }

  return (
    <Box sx={{ maxWidth: 960, mx: 'auto', mt: 4, p: 2 }}>
      {/* Page Title */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h1" sx={h1}>
          My List
        </Typography>
        <Chip
          label={`${items.length} ${items.length === 1 ? 'Title' : 'Titles'}`}
          color="primary"
          variant="outlined"
          sx={{ fontWeight: 'bold' }}
        />
      </Box>

      {/* Error Banner */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} data-testid="qa-list_error-error">
          {error}
        </Alert>
      )}

      {/* Controls Bar: Search & Sort */}
      <Box sx={{ display: 'flex', gap: 2, mb: 3, flexWrap: 'wrap' }}>
        <TextField
          label="Search within list"
          variant="outlined"
          size="small"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          sx={{ flexGrow: 1, minWidth: 220 }}
          data-testid="qa-list_search-input"
          inputProps={{ 'data-testid': 'qa-list_search-input' }}
        />
        <FormControl size="small" sx={{ minWidth: 200 }}>
          <InputLabel id="list-sort-select-label">Sort By</InputLabel>
          <Select
            labelId="list-sort-select-label"
            id="list-sort-select"
            value={sortBy}
            label="Sort By"
            onChange={(e) => setSortBy(e.target.value)}
            data-testid="qa-list_sort-select"
          >
            <MenuItem value="updated_desc">Recently Updated</MenuItem>
            <MenuItem value="rating_desc">Highest Rated</MenuItem>
            <MenuItem value="rating_asc">Lowest Rated</MenuItem>
            <MenuItem value="title_asc">Title (A-Z)</MenuItem>
            <MenuItem value="title_desc">Title (Z-A)</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {/* Status Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs
          value={activeTab}
          onChange={(_, val) => setActiveTab(val)}
          variant="scrollable"
          scrollButtons="auto"
        >
          {TAB_STATUSES.map((tab) => (
            <Tab
              key={tab.key}
              value={tab.key}
              label={
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <span>{tab.label}</span>
                  <Chip
                    label={statusCounts[tab.key] ?? 0}
                    size="small"
                    sx={{ height: 20, fontSize: '0.72rem' }}
                  />
                </Box>
              }
              data-testid={`qa-list_tab_${tab.key}-click`}
            />
          ))}
        </Tabs>
      </Box>

      {/* Loading Indicator */}
      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 6 }} data-testid="qa-list_loading-loading">
          <CircularProgress />
        </Box>
      )}

      {/* Empty State */}
      {!loading && filteredItems.length === 0 && (
        <Card sx={{ p: 5, textAlign: 'center', background: '#181b20', border: '1px dashed #334155' }} data-testid="qa-list_empty-empty">
          <Typography variant="h5" sx={{ mb: 1, color: '#94a3b8' }}>
            {searchQuery
              ? 'No anime found matching your search.'
              : activeTab === 'all'
              ? 'Your list is empty.'
              : `No anime currently marked as "${TAB_STATUSES.find((t) => t.key === activeTab)?.label}".`}
          </Typography>
          <Typography variant="body2" sx={{ color: '#64748b', mb: 3 }}>
            Explore the catalog and add titles to your personal anime list.
          </Typography>
          <Button
            variant="contained"
            component={Link}
            to="/get-anime"
            data-testid="qa-list_browse_anime-click"
          >
            Browse Anime
          </Button>
        </Card>
      )}

      {/* Items Collection */}
      {!loading && filteredItems.length > 0 && (
        <Stack spacing={2} data-testid="qa-list_items-list">
          {filteredItems.map((item) => (
            <Card
              key={item.id}
              sx={{
                p: 2.5,
                background: '#1a1e24',
                border: '1px solid #2e3440',
                display: 'flex',
                flexDirection: 'column',
                gap: 1.5,
              }}
              data-testid="qa-list_item-card"
            >
              {/* Card Top Row: Title, Metadata, Actions */}
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 1 }}>
                <Box sx={{ flexGrow: 1, minWidth: 260 }}>
                  <Link
                    to={`/anime/${item.anime_id}/details`}
                    style={{ textDecoration: 'none', color: '#60a5fa' }}
                    data-testid="qa-list_item_title-click"
                  >
                    <Typography variant="h5" sx={{ fontWeight: 700, '&:hover': { textDecoration: 'underline' } }}>
                      {item.anime.title}
                    </Typography>
                  </Link>
                  {item.anime.jp_title && (
                    <Typography variant="caption" sx={{ color: '#94a3b8', display: 'block' }}>
                      {item.anime.jp_title}
                    </Typography>
                  )}
                  <Stack direction="row" spacing={1} sx={{ mt: 0.8 }}>
                    <Chip label={item.anime._type.toUpperCase()} size="small" variant="outlined" />
                    <Chip label={item.anime.content_rating} size="small" variant="outlined" />
                  </Stack>
                </Box>

                {/* Status Selector & Remove Button */}
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
                  <FormControl size="small" sx={{ minWidth: 160 }}>
                    <Select
                      value={item.status}
                      onChange={(e) => handleStatusChange(item.anime_id, e.target.value as ListStatus)}
                      data-testid="qa-list_status-select"
                      sx={{ fontSize: '0.88rem' }}
                    >
                      <MenuItem value="watching">Watching</MenuItem>
                      <MenuItem value="plan_to_watch">Plan to Watch</MenuItem>
                      <MenuItem value="complete">Complete</MenuItem>
                      <MenuItem value="on_hold">On Hold</MenuItem>
                      <MenuItem value="dropped">Dropped</MenuItem>
                    </Select>
                  </FormControl>
                  <IconButton
                    color="error"
                    size="small"
                    onClick={() => handleRemove(item.anime_id)}
                    title="Remove from list"
                    data-testid="qa-list_remove-click"
                  >
                    <DeleteOutlineIcon fontSize="small" />
                  </IconButton>
                </Box>
              </Box>

              <Divider sx={{ borderColor: '#2e3440' }} />

              {/* Card Bottom Row: Ratings & Re-rate Action */}
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
                  {/* Community Rating */}
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                    <StarIcon sx={{ fontSize: 18, color: '#f59e0b' }} />
                    <Typography variant="body2" sx={{ color: '#94a3b8' }}>
                      Community:
                    </Typography>
                    <Typography variant="body2" sx={{ fontWeight: 700 }} data-testid="qa-list_community_rating-data">
                      {item.anime.rating ? `${item.anime.rating} / 10` : 'None'}
                    </Typography>
                  </Box>

                  {/* User Personal Rating */}
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                    <StarBorderIcon sx={{ fontSize: 18, color: '#38bdf8' }} />
                    <Typography variant="body2" sx={{ color: '#94a3b8' }}>
                      Your Rating:
                    </Typography>
                    <Typography
                      variant="body2"
                      sx={{ fontWeight: 700, color: item.user_rating ? '#38bdf8' : '#64748b' }}
                      data-testid="qa-list_user_rating-data"
                    >
                      {item.user_rating ? `${item.user_rating.rating} / 10` : 'Unrated'}
                    </Typography>
                  </Box>
                </Box>

                {/* Re-rate Button */}
                <Button
                  variant="outlined"
                  size="small"
                  startIcon={<EditIcon />}
                  onClick={() => openReRateModal(item)}
                  data-testid="qa-list_re_rate-click"
                >
                  {item.user_rating ? 'Re-rate' : 'Rate Show'}
                </Button>
              </Box>

              {/* User Rating Comment Display */}
              {item.user_rating?.comment && (
                <Box sx={{ background: '#12151a', p: 1.2, borderRadius: 1, borderLeft: '3px solid #38bdf8' }}>
                  <Typography variant="caption" sx={{ color: '#94a3b8', fontStyle: 'italic' }}>
                    "{item.user_rating.comment}"
                  </Typography>
                </Box>
              )}
            </Card>
          ))}
        </Stack>
      )}

      {/* Re-Rate Modal Dialog */}
      <Dialog
        open={reRateItem !== null}
        onClose={() => setReRateItem(null)}
        maxWidth="sm"
        fullWidth
        data-testid="qa-list_rating_dialog-dialog"
      >
        <DialogTitle>
          Rate {reRateItem?.anime.title}
        </DialogTitle>
        <DialogContent dividers>
          {ratingModalError && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {ratingModalError}
            </Alert>
          )}

          <Box sx={{ mb: 3 }}>
            <FormControl fullWidth sx={{ mt: 1 }}>
              <InputLabel id="re-rate-score-label">Rating Score (1 - 10)</InputLabel>
              <Select
                labelId="re-rate-score-label"
                id="re-rate-score"
                value={ratingScore}
                label="Rating Score (1 - 10)"
                onChange={(e) => setRatingScore(Number(e.target.value))}
                data-testid="qa-list_rating_score-select"
              >
                {[10, 9, 8, 7, 6, 5, 4, 3, 2, 1].map((score) => (
                  <MenuItem key={score} value={score}>
                    {score} / 10 — {RATING_DESCRIPTIONS[score]}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>

          <TextField
            fullWidth
            label="Comment / Blurb (Optional)"
            multiline
            rows={3}
            value={ratingComment}
            onChange={(e) => setRatingComment(e.target.value)}
            helperText={`${ratingComment.length}/500 characters`}
            inputProps={{ maxLength: 500, 'data-testid': 'qa-list_rating_comment-input' }}
            data-testid="qa-list_rating_comment-input"
          />
        </DialogContent>
        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setReRateItem(null)} color="inherit" disabled={savingRating}>
            Cancel
          </Button>
          <Button
            onClick={handleSaveRating}
            variant="contained"
            color="primary"
            disabled={savingRating}
            data-testid="qa-list_rating_save-submit"
          >
            {savingRating ? <CircularProgress size={22} /> : 'Save Rating'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default UserList;

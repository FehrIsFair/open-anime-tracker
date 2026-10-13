export type ListStatus =
  | 'plan_to_watch'
  | 'watching'
  | 'complete'
  | 'dropped'
  | 'on_hold';

export const STATUS_LABELS: Record<ListStatus, string> = {
  watching: 'Watching',
  plan_to_watch: 'Plan to Watch',
  complete: 'Complete',
  on_hold: 'On Hold',
  dropped: 'Dropped',
};

export const ALL_STATUSES: ListStatus[] = [
  'watching',
  'plan_to_watch',
  'complete',
  'on_hold',
  'dropped',
];

export interface UserListItem {
  id: number;
  anime_id: number;
  user_id: number;
  status: ListStatus;
  created_at: string | null;
  updated_at: string | null;
  anime: {
    id: number;
    title: string;
    jp_title?: string | null;
    desc?: string | null;
    _type: string;
    rating: number | null;
    content_rating: string;
  };
  user_rating?: {
    id: number;
    rating: number;
    comment?: string | null;
  } | null;
}

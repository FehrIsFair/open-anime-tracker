import _ from 'lodash'


export interface Anime {
  title: string;
  jp_title: string;
  _type: string;
  seasons: number;
  rating: number | any;
  episodes: number;
  desc: string;
  status: string;
  nsfw: boolean;
  content_rating: string
}

export const to_json = (object: Anime): any => {
  return _(object).toJSON()
}

export interface UserRatingRecord {
  id: number;
  user_id: number;
  rating: number;
  comment: string | null;
  anime_id: number;
  season_id: number | null;
  created_at?: string | null;
  updated_at?: string | null;
}

export interface ReviewItem {
  id: number;
  user_id: number;
  username: string;
  rating: number;
  comment: string | null;
  anime_id: number;
  season_id: number | null;
  season_title?: string | null;
  created_at?: string | null;
  updated_at?: string | null;
}

export default Anime
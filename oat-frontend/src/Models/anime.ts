import _ from 'lodash'
import { MaybeNumber } from '../extentsions/helper_funcs';

export interface Anime {
  title: string;
  jp_title: string;
  _type: string;
  seasons: array<any>;
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

export default Anime

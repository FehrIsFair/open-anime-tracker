import _ from 'lodash'

export interface Anime {
  title: string;
  jp_title: string;
  other_titles: any;
  rating: number;
  type: string;
  seasons: number;
  episodes: number;
  desc: string;
  status: string;
}

export const to_json = (object: Anime): any => {
  return _(object).toJSON()
}

export default Anime
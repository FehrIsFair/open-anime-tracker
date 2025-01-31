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

export default Anime
import _ from 'lodash'
import { MaybeNumber } from '../extentsions/helper_funcs'

export interface Season {
  title: string;
  season_number: number;
  type_season: string;
  part: number;
  desc: string;
  rating: number;
}

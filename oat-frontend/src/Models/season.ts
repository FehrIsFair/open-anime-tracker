export interface Season {
  id: number;
  season_number: number;
  title: string | null;
  episodes: number | null;
  desc: string | null;
  rating: number | null;
  air_date: string | null;
  end_date: string | null;
  type_season: string;
  part: number | null;
}

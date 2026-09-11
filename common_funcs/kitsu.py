from requests import request

from const import kitsu_api_base, kitsu_headers
from database import session
from db_models.anime import Anime
from db_models.seasons import Seasons
from enums.db_enums import AnimeType, ReviewStatus, SeasonType


class KitsuAPIError(Exception):
  """Raised when the Kitsu API returns an error."""


class KitsuDataError(Exception):
  """Raised when Kitsu API response is missing required data."""


def _fetch_kitsu_data(kitsu_id: int) -> dict:
  """Fetch raw anime data from Kitsu API."""
  res = request('GET', f'{kitsu_api_base}/anime/{kitsu_id}', headers=kitsu_headers)

  if res.status_code == 404:
    raise KitsuAPIError('Anime not found on Kitsu')

  res.raise_for_status()

  try:
    data = res.json()['data']['attributes']
  except (KeyError, ValueError) as e:
    raise KitsuDataError('Malformed response from Kitsu API') from e

  return data


def _parse_anime_kwargs(data: dict) -> dict:
  """Parse Kitsu anime data into kwargs for the Anime model."""
  titles = data.get('titles', {})

  anime_kwargs = {
    'title': titles.get('en'),
    'jp_title': titles.get('ja_jp'),
    'other_titles': {k: v for k, v in titles.items() if k not in ('en', 'ja_jp')},
    'desc': data.get('description') or data.get('synopsis'),
    'content_rating': data.get('ageRating', 'PG'),
    'air_date': data.get('startDate'),
    'end_date': data.get('endDate'),
    'episodes': data.get('episodeCount'),
  }

  # Map Kitsu type to AnimeType
  kitsu_type = data.get('type', '')
  if kitsu_type == 'movie':
    anime_kwargs['_type'] = AnimeType.movie
  else:
    anime_kwargs['_type'] = AnimeType.show

  # Parse rating if available
  avg_rating = data.get('averageRating')
  if avg_rating:
    try:
      anime_kwargs['rating'] = float(avg_rating)
    except (ValueError, TypeError):
      pass

  return anime_kwargs


def _parse_season_kwargs(data: dict) -> dict:
  """Parse Kitsu anime data into kwargs for the Seasons model (season 1)."""
  return {
    'episodes': data.get('episodeCount'),
    'desc': data.get('description') or data.get('synopsis'),
    'air_date': data.get('startDate'),
    'end_date': data.get('endDate'),
    'type_season': SeasonType.SPECIAL,
    'title': data.get('titles', {}).get('en'),
  }


def import_seasons_to_anime(anime_id: int, seasons: list[dict]) -> dict:
  """Create multiple Seasons records for an existing Anime.

  Fetches data from Kitsu API for each season's kitsuId and populates
  season fields (desc, episodes, title, air_date, end_date).

  Args:
    anime_id: The ID of the existing anime to attach seasons to.
    seasons: List of dicts with keys seasonNumber, kitsuId, typeSeason,
             hasParts, part.

  Returns a dict with keys: id, title, message, seasonsCreated.
  Raises RuntimeError if anime not found, DB fails, or a Kitsu ID is invalid.
  """
  if not seasons:
    raise ValueError('At least one season is required')

  anime = session.query(Anime).filter(Anime.id == anime_id).first()
  if not anime:
    raise RuntimeError('Anime not found')

  for season_data in seasons:
    # Fetch real data from Kitsu API
    kitsu_data = _fetch_kitsu_data(season_data['kitsuId'])
    season_kwargs = _parse_season_kwargs(kitsu_data)

    type_season_str = season_data.get('typeSeason', 'season').lower()
    try:
      type_season = SeasonType(type_season_str)
    except ValueError:
      type_season = SeasonType.SEASON

    # Remove type_season from kwargs — we override it with the user's selection
    season_kwargs.pop('type_season', None)

    season = Seasons(
      season_number=season_data['seasonNumber'],
      anime_id=anime_id,
      **season_kwargs,
      type_season=type_season,
      part=season_data.get('part'),
    )
    session.add(season)

  try:
    session.commit()
  except Exception as e:
    session.rollback()
    raise RuntimeError('Failed to save seasons to database') from e

  return {
    'id': anime.id,
    'title': anime.title,
    'message': f"{len(seasons)} season(s) added to \"{anime.title}\"",
    'seasonsCreated': len(seasons),
  }


def fetch_and_store_kitsu_anime(kitsu_id: int) -> dict:
  """Fetch anime from Kitsu, create Anime + Seasons records, commit.

  Returns a dict with keys: id, title, message.
  Raises KitsuAPIError, KitsuDataError, or ValueError for invalid input.
  """
  if not isinstance(kitsu_id, int) or kitsu_id <= 0:
    raise ValueError('kitsuId must be a positive integer')

  data = _fetch_kitsu_data(kitsu_id)
  anime_kwargs = _parse_anime_kwargs(data)

  # Ensure title exists
  if not anime_kwargs.get('title'):
    raise KitsuDataError('Anime has no title in Kitsu data')

  anime = Anime(
    title=anime_kwargs.pop('title'),
    _type=anime_kwargs.pop('_type'),
    status=ReviewStatus.confirmed,
    **anime_kwargs,
  )
  session.add(anime)
  session.flush()  # get the anime.id without committing

  season_kwargs = _parse_season_kwargs(data)

  season = Seasons(
    season_number=1,
    anime_id=anime.id,
    **season_kwargs,
  )
  session.add(season)

  try:
    session.commit()
  except Exception as e:
    session.rollback()
    raise RuntimeError('Failed to save anime to database') from e

  return {
    'id': anime.id,
    'title': anime.title,
    'message': f'Anime "{anime.title}" imported successfully',
  }

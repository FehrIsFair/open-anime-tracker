import pdb

from numpy._core.strings import isnumeric
from requests import request
import sys
import json
import ast

from const import kitsu_api_base,  kitsu_headers
from database import session
from db_models.anime import Anime
from db_models.seasons import Seasons
from enums.db_enums import SeasonType, AnimeType, ReviewStatus


def get_title_dict(x: dict) -> dict:
  return_dict = {}
  for key, value in x.items():
    if key not in ['en', 'ja_jp']:
      return_dict[key] = value
  return return_dict


if __name__ == 'main':
  anime_id: int = 0
  season_ids: [int] = []
  args = sys.argv

  for arg in args:
    if 'id' in arg:
      anime_id = int(arg)
    if 'seasons' in arg:
      ids = arg.split('=')[1].split(',')
      for _id in ids:
        season_ids.append(_id)

  res = request('GET', f'{kitsu_api_base}/anime/{anime_id}', headers=kitsu_headers)

  json: dict = ast.literal_eval(res._content.decode('utf-8'))['data']

  anime_kwargs = {
    'desc': json['attributes']['description'],
    'air_date': json['attributes']['startDate'],
    'end_date': json['attributes']['endDate'],
    'type_season': SeasonType.SPECIAL,
    'part': None
  }
  anime = Anime(json['attributes']['titles']['en'], AnimeType.show.value, ReviewStatus.confirmed, **anime_kwargs)
  session.add(anime)
  session.commit()

  new_anime = session.query(Anime).filter(anime.title == Anime.title).first()

  for i, _id in enumerate(season_ids):
    season_number = 0
    part = None
    res = request('GET', f'{kitsu_api_base}/anime/{_id}', headers=kitsu_headers)
    json: dict = ast.literal_eval(res._content.decode('utf-8'))
    if 'Part' in json['attributes']['titles']['en']:
      part = int(json['attributes']['titles']['en'].split('Part ')[1])
      season_number = i - 1
    kwargs = {
      'desc': json['attributes']['description'],
      'air_date': json['attributes']['startDate'],
      'end_date': json['attributes']['endDate'],
      'type_season': SeasonType.SPECIAL,
      'part': part
    }
    season = Seasons(i if part is None else season_number, new_anime.id, json['attributes']['episodeCount'], **kwargs)
    session.add(season)
    session.commit()

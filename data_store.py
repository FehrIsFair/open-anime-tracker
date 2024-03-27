import json
import pdb

from main import db, session
from db_models.anime import Anime
from enums.db_enums import AnimeType, ReviewStatus
from db_models.seasons import Seasons

def get_title_dict(x: dict) -> dict:
  return_dict = {}
  for key, value in x.items():
    if key not in ['en', 'ja_jp']:
      return_dict[key] = value
  return return_dict

with open('./data/test_data.json') as json_file:
  data = json.load(json_file)['data']

  kwargs = {
    'jp_title': data['attributes']['titles']['ja_jp'],
    'other_titles': get_title_dict(data['attributes']['titles']),
    'seasons': 7,
    'desc': data['attributes']['description']
  }

  anime = Anime(data['attributes']['titles']['en'], AnimeType.show.value, ReviewStatus.CONFIRMED, **kwargs)

  session.add(anime)
  session.commit()

import json

from data_pull import get_title_dict
from database import session
from db_models.anime import Anime
from db_models.seasons import Seasons
from enums.db_enums import AnimeType, ReviewStatus, SeasonType

anime_ids = ['13569', '41982']



anime_data = {}


with open('./data/47132.json') as json_file:
  data = json.load(json_file)['data']


  kwargs = {
    'desc': data['attributes']['description'],
    'air_date': data['attributes']['startDate'],
    'end_date': data['attributes']['endDate'],
    'type_season': SeasonType.SPECIAL,
    'part': 4
  }

  season = Seasons(4, 1, data['attributes']['episodeCount'], **kwargs)

  session.add(season)
  session.commit()

  kwargs = {
    'jp_title': data['attributes']['titles']['ja_jp'],
    'other_titles': get_title_dict(data['attributes']['titles']),
    'seasons': 7,
    'desc': data['attributes']['description'],
    'content_rating': data['attributes']['ageRating']
  }

  anime = Anime(data['attributes']['titles']['en'], AnimeType.show.value, ReviewStatus.confirmed, **kwargs)

  session.add(anime)
  session.commit()

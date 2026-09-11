from flask import Blueprint, make_response, request
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from database import session
from db_models.anime import Anime
from db_models.seasons import Seasons
from enums.db_enums import AnimeType, ReviewStatus
from project_exceptions.exceptions import InvalidEnumException

anime_routes = Blueprint('anime', __name__)


def get_anime_type(input: str):
  match input:
    case AnimeType.show.value:
      return AnimeType.show
    case AnimeType.movie.value:
      return AnimeType.movie
    case _:
      raise InvalidEnumException(f'Value: {input} is not a valid Anime Type')


def get_review_type(input: str):
  match input:
    case ReviewStatus.pending.value:
      return ReviewStatus.pending
    case ReviewStatus.confirmed.value:
      return ReviewStatus.confirmed
    case ReviewStatus.quarantine.value:
      return ReviewStatus.quarantine
    case _:
      raise InvalidEnumException(f'Value: {input} is not a valid Review Status')


@anime_routes.route('/anime', methods=['GET'])
def index():
  return_dict = {}
  try:
    req_anime = session.query(Anime).all()
  except SQLAlchemyError as e:
    print(e)
    return make_response({'Message': 'Failed to fetch anime'}, 500)
  return_dict['data'] = [a.make_json() for a in req_anime]

  return make_response(return_dict, 200)


@anime_routes.route('/anime/<int:anime_id>', methods=['GET'])
def get_anime_by_id(anime_id):
  try:
    anime = session.query(Anime).filter(Anime.id == anime_id).first()
    if not anime:
      return make_response({'message': 'Anime not found'}, 404)
    seasons = session.query(Seasons).filter(Seasons.anime_id == anime_id).all()
    season_list = []
    for s in seasons:
      season_dict = {}
      for key, value in s.__dict__.items():
        if key == '_sa_instance_state':
          continue
        if key == 'type_season':
          season_dict[key] = value.value if hasattr(value, 'value') else value
        else:
          season_dict[key] = value
      season_list.append(season_dict)
    return make_response({'anime': anime.make_json(), 'seasons': season_list}, 200)
  except SQLAlchemyError as e:
    print(e)
    return make_response({'message': 'Failed to fetch anime details'}, 500)


@anime_routes.route('/anime/search', methods=['GET'])
def search_anime():
  q = request.args.get('q', '')
  if len(q) < 2:
    return make_response({'message': 'Query must be at least 2 characters'}, 400)

  try:
    query = f'%{q.lower()}%'
    results = session.query(Anime).filter(func.lower(Anime.title).like(query)).limit(10).all()
    return make_response({'anime': [a.make_json() for a in results]}, 200)
  except SQLAlchemyError as e:
    print(e)
    return make_response({'message': 'Failed to search anime'}, 500)


@anime_routes.route('/anime/create', methods=['POST'])
def create_anime():
  request_json = request.get_json()
  anime = session.query(Anime).filter(Anime.title == request_json['title']).first()

  if anime:
    return make_response({'Message': 'Anime Already Exists'}, 409)

  kwargs = {}

  for key, value in request_json.items():
    if key not in ['title', '_type', 'status']:
      kwargs[key] = value

  try:
    _type = get_anime_type(request_json['_type'])
    status = get_review_type(request_json['status'])
  except InvalidEnumException:
    return make_response({'Message': 'Failed to Properly Set Enum Type'}, 500)

  anime = Anime(request_json['title'], _type, status, **kwargs)

  try:
    session.add(anime)
    session.commit()
  except SQLAlchemyError as e:
    print(e)
    return make_response({'Message': 'Failed to create anime'}, 500)

  return make_response({'Message': 'Anime Successfully Created'}, 200)


@anime_routes.route('/anime/edit', methods=['PATCH'])
def edit_anime():
  request_json = request.get_json()
  anime = session.query(Anime).filter(Anime.id == request_json['data']['_id']).first()

  if not anime:
    return make_response({'Message': 'Anime Does not exits'}, 404)

  kwargs = {}
  for key, value in request_json['data'].items():
    if key in request_json['diffs']:
      kwargs[key] = value

  anime.set_values(**kwargs)

  try:
    session.commit()
  except SQLAlchemyError as e:
    print(e)
    return make_response({'Message': 'Failed to commit changes to Anime'}, 500)
  return make_response({'Message': 'Anime Updated'}, 200)


@anime_routes.route('/anime/delete', methods=['DELETE'])
def delete_anime():
  request_json = request.get_json()
  anime = session.query(Anime).filter(Anime.id == request_json['data']['_id']).first()

  if not anime:
    return make_response({'Message': 'Anime Does not exits'}, 404)

  anime.delete()

  try:
    session.commit()
  except SQLAlchemyError as e:
    print(e)
    return make_response({'Message': 'Could not delete anime'}, 500)
  return make_response({'Message': 'Anime Successfully deleted'}, 200)

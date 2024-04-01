import pdb

from flask import request, Blueprint, Response, make_response
from flask_cors import cross_origin

from database import session
from db_models.anime import Anime
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
@cross_origin(origin="localhost", headers=['Content-Type', 'Authorization'])
def index():
  return_dict = {}
  try:
    req_anime = session.query(Anime).all()
  except Exception as e:
    print(e)
    return make_response({'Message': 'Failed to fetch anime'}, 500)
  return_dict['data'] = [a.make_json() for a in req_anime]

  return make_response(return_dict, 200)


@anime_routes.route('/anime/create', methods=['POST'])
@cross_origin(origin="localhost", headers=['Content-Type', 'Authorization'])
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
  except Exception as e:
    print(e)
    return make_response({'Message': 'Failed to create anime'}, 500)

  return make_response({'Message': 'Anime Successfully Created'}, 200)


@anime_routes.route('/anime/edit', methods=['PATCH'])
@cross_origin(origin="localhost", headers=['Content-Type', 'Authorization'])
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
  except Exception as e:
    print(e)
    return make_response({'Message': 'Failed to commit changes to Anime'}, 500)
  return make_response({'Message': 'Anime Updated'}, 200)


@anime_routes.route('/anime/delete', methods=['DELETE'])
@cross_origin(origin="localhost", headers=['Content-Type', 'Authorization'])
def delete_anime():
  request_json = request.get_json()
  anime = session.query(Anime).filter(Anime.id == request_json['data']['_id']).first()

  if not anime:
    return make_response({'Message': 'Anime Does not exits'}, 404)

  anime.delete()

  try:
    session.commit()
  except Exception as e:
    print(e)
    return make_response({'Message': 'Could not delete anime'}, 500)
  return make_response({'Message': 'Anime Successfully deleted'}, 200)

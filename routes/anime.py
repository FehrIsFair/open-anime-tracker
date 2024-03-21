import pdb

from flask import request, Blueprint, Response
from flask_cors import cross_origin

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
    case ReviewStatus.PENDING.name:
      return ReviewStatus.PENDING
    case ReviewStatus.CONFIRMED.name:
      return ReviewStatus.CONFIRMED
    case ReviewStatus.QUARANTINE.name:
      return ReviewStatus.QUARANTINE
    case _:
      raise InvalidEnumException(f'Value: {input} is not a valid Review Status')


@anime_routes.route('/anime', methods=['GET'])
@cross_origin(origin="localhost", headers=['Content-Type', 'Authorization'])
def index():
  return Response(response="Route Not found", status=404, content_type='application/json')


@anime_routes.route('/anime/create', methods=['POST'])
@cross_origin(origin="localhost", headers=['Content-Type', 'Authorization'])
def create_anime():
  from main import db
  request_json = request.get_json()
  anime = db.session.query(Anime).filter(Anime.title == request_json['title']).first()
  if anime:
    return Response(response='Anime already exists', status=409, content_type="application/json")

  kwargs = {}
  for key, value in request_json.items():
    if key not in ['title', '_type', 'status']:
      kwargs[key] = value
  try:
    _type = get_anime_type(request_json['_type'])
    status = get_review_type(request_json['status'])
  except InvalidEnumException:
    return Response(response=f'Failed to properly set enum type', status=500, content_type='application/json')
  anime = Anime(request_json['title'], _type, **kwargs)
  try:
    db.session.add(anime)
    db.session.commit()
  except Exception as e:
    print(e)
    return Response(response="Failed to create Anime", status=500, content_type="application/json")
  return Response(response='Anime Successfully created',  status=200, content_type="application/json")



# class AnimeView(FlaskView):
#
#   def index(self):
#     return 404
#
#   def get(self, _id: int):
#     anime = db.session.query(Anime).filter(Anime.id == _id).first()
#     if not anime:
#       return 404, "Anime not found"
#     return {'anime': anime}
#
#   def put(self):
#     request_json = request.get_json()['data']
#     anime = db.session.query(Anime).filter(Anime.id == request_json['id']).first()
#     for key in request_json.keys():
#       anime.__dict__[key] = request_json[key]
#     try:
#       db.session.commit()
#     except Exception as e:
#       return 500, f"Encountered: {e}"
#     return 200, {'anime': anime, "message": "Anime updated"}
#
#   def post(self):
#     request_json = request.get_json()['data']
#     anime = db.session.query().filter(Anime.title == request_json['anime']).first()
#     if anime:
#       return 409, "Anime already exists"
#     kwargs = {}
#     for key, value in request_json.items():
#       if key not in ['title', '_type', 'status']:
#         kwargs[key] = value
#     anime = Anime(request_json['title'], request_json['_type'], request_json['status'], **kwargs)
#     try:
#       db.session.add(anime)
#       db.session.commit()
#     except Exception as e:
#       return 500, "Anime Failed to Create"
#     return 200, {'anime': anime, 'message': "Anime Successfully Created"}
#
#   def delete(self):
#     request_json = request.get_json()['data']
#     anime = db.session.query(Anime).filter(Anime.id == request_json['id']).first()
#     if not anime:
#       return 404, "Anime not found"
#     db.session.delete(anime)
#     try:
#       db.session.commit()
#     except Exception as e:
#       return 500, "Anime could not be deleted."
#     return 200, "Anime was deleted successfully."

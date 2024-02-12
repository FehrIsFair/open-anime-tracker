from flask import MethodView, request
from sqlalchemy import db
from db_models.anime import Anime
from flask_classful import FlaskView


class AnimeView(FlaskView):
  route_base = 'anime'

  def index(self):
    return 404

  def get(self, _id: int):
    anime = db.session.query(Anime).filter(Anime.id == _id).first()
    if not anime:
      return 404, "Anime not found"
    return {'anime': anime}

  def put(self):
    request_json = request.get_json()['anime']
    anime = db.session.query(Anime).filter(Anime.id == request_json['id']).first()
    for key in request_json.keys():
      anime.__dict__[key] = request_json[key]
    try:
      db.session.commit()
    except Exception as e:
      return 500, f"Encountered: {e}"
    return 200, {'anime': anime, "message": "Anime updated"}

  def post(self):
    request_json = request.get_json()['anime']
    anime = db.session.query().filter(Anime.title == request_json['anime']).first()
    if anime:
      return 409, "Anime already exists"
    kwargs = {}
    for key, value in request_json.items():
      if key not in ['title', '_type', 'status']:
        kwargs[key] = value
    anime = Anime(request_json['title'], request_json['_type'], request_json['status'], **kwargs)
    try:
      db.session.add(anime)
      db.session.commit()
    except Exception as e:
      return 500, "Anime Failed to Create"
    return 200, {'anime': anime, 'message': "Anime Successfully Created"}

  def delete(self):
    request_json = request.get_json()['anime']
    anime = db.session.query(Anime).filter(Anime.id == request_json['id']).first()
    if not anime:
      return 404, "Anime not found"
    db.session.delete(anime)
    try:
      db.session.commit()
    except Exception as e:
      return 500, "Anime could not be deleted."
    return 200, "Anime was deleted successfully."

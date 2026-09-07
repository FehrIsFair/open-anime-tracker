from operator import and_

from flask_classful import FlaskView
from sqlalchemy import db
from sqlalchemy.exc import SQLAlchemyError

from db_models.anime import Anime
from db_models.list import List


class ListView(FlaskView):
  route_base = 'list'

  def index(self):
    return 404

  def get(self, _id: int):
    lists = db.session.query(List).filter(List.id == _id).first()
    anime_list = []
    if not lists:
      return 404, "List not found."
    for list in lists:
      anime = db.session.query(Anime).filter(Anime.id == list.anime_id).first()
      anime_list.append(anime)
    if not anime_list:
      return 404, "List not found"
    return {'list': anime_list}

  def post(self, anime_id, user_id):
    list = List(anime_id, user_id)
    try:
      db.session.add(list)
      db.session.commit()
    except SQLAlchemyError:
      return 500, "Anime could not be added to the list"
    return 200, {'Saved to List'}

  def delete(self, anime_id, user_id):
    list = db.session.query(List).filter(and_(List.anime_id == anime_id, List.user_id == user_id)).first()
    if not list:
      return 404, "Anime not in list"
    db.session.delete(list)
    try:
      db.session.commit()
    except SQLAlchemyError:
      return 500, "Anime could not be removed from the list"
    return 200, "Anime was removed from the list"

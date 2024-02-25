import const
from operator import and_

from flask import MethodView, request
from sqlalchemy import db
from db_models.users import User
from flask_classful import FlaskView
from helper_funcs import bcrypt


class UserView(FlaskView):
  route_base = 'users'

  def index(self):
    users = db.session.query(User).all()
    return 200, {'users': users}

  def get(self, user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    if not user:
      return 404, "User not found."
    return 200, {'user': user}

  def put(self):
    request_json = request.get_json()
    user = db.session.query(User).filter(User.id == request_json['user_id']).first()
    if not user:
      return 404, 'User not found'
    if bcrypt.check_password_hash(user.password, request_json['old_pw']):
      user.password = bcrypt.generate_password_hash(request_json['password'], const.SALT).decode('utf-8')
      db.session.commit()
      return 200, "Password successfully updated."
    else:
      return 401, "Old Password did not match. Cannot update password."

  def post(self):
    request_json = request.get_json()
    user = db.session.query(User).filter(User.id == request_json['email']).first()
    if not user:
      return 409, "User already exists"
    hash = bcrypt.generate_password_hash(request_json['password'], os.environ.get('SALT')).decode('utf-8')
    new_user = User(request_json['email'], hash)
    try:
      db.session.add(new_user)
      db.session.commit()
    except Exception as e:
      return 500, "Could not Create User"
    return 200, "User Create Successfully"

  def delete(self):
    request_json = request.get_json()
    user = db.session.query(User).filter(User.id == request_json['user_id']).first()
    if not user:
      return 404, "User not found."
    db.session.delete(user)
    try:
      db.session.commit()
    except Exception as e:
      return 500, "Could not delete user."
    return 200, "User deleted"

import datetime
import os
import pdb
from passlib.hash import bcrypt as bc

from flask import request, Blueprint, make_response
from flask_cors import cross_origin
from sqlalchemy import and_
# bcrypt in the functions is imported locally to avoid circular imports.


from database import session
from db_models.users import User

user_routes = Blueprint('user', __name__)


@user_routes.route('/user', methods=['GET'])
@cross_origin(origin="localhost", headers=['Content-Type', 'Authorization'])
def index():
  return_list = []
  try:
    req_user = session.query(User).all()
  except Exception as e:
    print(e)
    return make_response({'Message': 'Could not find users'}, 500)

  return_list = [u.make_json() for u in req_user]

  return make_response({'data': return_list}, 200)


@user_routes.route('/user/create', methods=['POST'])
@cross_origin(origin="localhost", headers=['Content-Type', 'Authorization'])
def create_user():
  json = request.get_json()
  user = session.query(User).filter(and_(User.email == json['email'], User.username == json['username'])).first()

  if user:
    return make_response({'Message': 'User already exists with email, username combo'}, 409)
  hash_ = bc.using(int(os.environ.get('SALT'))).hash(json['password'])

  new_user = User(json['email'], hash_, json['username'])

  try:
    session.add(new_user)
    session.commit()
  except Exception as e:
    print(e)
    return make_response({'Message': 'Could not create new user'}, 500)

  return make_response({'Message': 'User create successfully'}, 200)


@user_routes.route('/user/update_pw', methods=['PATCH'])
@cross_origin(origin="localhost", headers=['Content-Type', 'Authorization'])
def edit_user():
  json = request.get_json()
  user = session.query(User).filter(and_(User.id == json['id'])).first()

  if not user:
    return make_response({'Message': 'User not found'}, 500)
  from helper_funcs import bcrypt
  old_hash = bcrypt.generate_password_hash(json['old_password'], os.environ.get('SALT')).decode('utf-8')
  if user.password != old_hash:
    return make_response({'Message': 'Old password did not match.'}, 500)

  new_hash = bcrypt.generate_password_hash(json['new_password'], os.environ.get('SALT')).decode('utf-8')

  user.password = new_hash

  try:
    session.commit()
  except Exception as e:
    print(e)
    return make_response({'Message': 'Could not update password'}, 500)
  return make_response({'Message': 'Password updated'}, 200)


@user_routes.route('/user/edit', methods=['PATCH'])
@cross_origin(origin="localhost", headers=['Content-Type', 'Authorization'])
def pw_update():
  json = request.get_json()
  user = session.query(User).filter(and_(User.id == json['id'])).first()

  if not user:
    return make_response({'Message': 'User not found'}, 404)

  from helper_funcs import bcrypt
  old_hash = bcrypt.generate_password_hash(json['password'], os.environ.get('SALT')).decode('utf-8')
  if user.password != old_hash:
    return make_response({'Message': 'Password did not match, will not update user'}, 500)

  kwargs = {}
  for key, value in json.items():
    if key != 'password':
      kwargs[key] = value

  user.set_values(**kwargs)

  try:
    session.commit()
  except Exception as e:
    print(e)
    return make_response({'Message': 'User could not be updated'}, 500)
  return make_response(({'Message': 'User updated.'}, 200))


@user_routes.route('/user/delete', methods=['DELETE'])
@cross_origin(origin="localhost", headers=['Content-Type', 'Authorization'])
def delete_user():
  json = request.get_json()
  user = session.query(User).filter(and_(User.id == json['id'])).first()

  if not user:
    return make_response({'Message': 'User not found'}, 404)

  user.deleted_at(datetime.datetime.utcnow())

  try:
    session.commit()
  except Exception as e:
    print(e)
    return make_response({'Message': 'Could not delete user'}, 500)

  return make_response({'Message': 'User Successfully deleted'}, 200)

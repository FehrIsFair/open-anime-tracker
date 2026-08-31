import bcrypt
from uuid import uuid4

from flask import request, Blueprint, make_response, jsonify, session as sesh

from database import session
from db_models.users import User

login_routes = Blueprint('auth', __name__)


@login_routes.route('/auth/login', methods=['POST'])
def login():
  json = request.get_json()
  user = session.query(User).filter(User.email == json['email']).first()
  if not user:
    return make_response({'Message': 'Invalid Username or Password'}, 401)
  if not bcrypt.checkpw(json['password'].encode('utf-8'), user.password.encode('utf-8')):
    return make_response({'Message': 'Invalid Username or Password'}, 401)
  uuid = str(uuid4())
  sesh[user.username] = uuid
  res = make_response(jsonify([user.username, user.email]), 200)
  return res


@login_routes.route('/auth/logout', methods=['POST'])
def logout():
  # Clear all session entries - the session cookie is sent automatically via HTTP
  for key in list(sesh.keys()):
    sesh.pop(key)
  return make_response({"Message": "Successful Logout"}, 200)


@login_routes.route('/auth/auth_check', methods=['POST'])
def check_auth():
  json = request.get_json()
  username = ''
  if json.get('cookie') in sesh:
    for key, value in sesh.items():
      if value == json['cookie']:
        username = key
        break
    user = session.query(User).filter(User.username == username).first()
    res = make_response(jsonify({'username': user.username, 'email': None, 'password': None}), 200)
    return res
  return make_response({'Message': 'User not authed'}, 401)

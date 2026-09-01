from uuid import uuid4

import bcrypt
from flask import Blueprint, jsonify, make_response, request
from flask import session as sesh

from database import session
from db_models.users import User

login_routes = Blueprint('auth', __name__)


@login_routes.route('/auth/login', methods=['POST'])
def login():
  json = request.get_json()
  user = session.query(User).filter(User.email == json['email']).first()
  if not user:
    return make_response({'Message': 'Invalid Username or Password'}, 401)
  if not bcrypt.checkpw(str(json['password']).encode('utf-8'), user.password.encode('utf-8')):
    return make_response({'Message': 'Invalid Username or Password'}, 401)
  uuid = str(uuid4())
  sesh['username'] = user.username
  sesh[str(user.username)] = uuid
  sesh['login_uuid'] = uuid
  sesh.modified = True
  res = make_response(jsonify([user.username, user.email]), 200)
  return res


@login_routes.route('/auth/login_as', methods=['POST'])
def login_as():
  """Create a session for an existing user (used after signup)."""
  json = request.get_json()
  user = session.query(User).filter(User.email == json['email']).first()
  if not user:
    return make_response({'Message': 'User not found'}, 404)
  uuid = str(uuid4())
  sesh['username'] = user.username
  sesh[str(user.username)] = uuid
  sesh['login_uuid'] = uuid
  sesh.modified = True
  res = make_response(jsonify([user.username, user.email]), 200)
  return res


@login_routes.route('/auth/validate', methods=['GET'])
def validate_session():
  """Verify current session user still exists in DB."""
  username = sesh.get('username')
  if not username:
    return make_response({'Message': 'No session'}, 401)
  user = session.query(User).filter(User.username == username).first()
  if not user:
    return make_response({'Message': 'User not found'}, 404)
  res = make_response(jsonify({'username': user.username, 'email': user.email}), 200)
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
    user: User | None = session.query(User).filter(User.username == username).first()
    if user is None:
        return make_response(jsonify({"Message": "user not found"}))
    res = make_response(jsonify({'username': user.username, 'email': None, 'password': None}), 200)
    return res
  return make_response({'Message': 'User not authed'}, 401)

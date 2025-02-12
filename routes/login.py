import pdb
import random
from datetime import datetime
import bcrypt
from uuid import uuid4
from werkzeug.http import dump_cookie

from flask import request, Blueprint, make_response, jsonify
from flask import session as sesh
from flask_cors import cross_origin

from database import session
from db_models.users import User


login_routes = Blueprint('auth', __name__)


@login_routes.route('/auth/login', methods=['POST'])
@cross_origin(origin="localhost", headers=['Content-Type', 'Authorization'])
def login():
  json = request.get_json()
  user = session.query(User).filter(User.email == json['email']).first()
  if not user:
    return make_response({'Message': 'Invalid Username or Password'}, 401)
  if not bcrypt.checkpw(json['password'].encode('utf-8'), user.password.encode('utf-8')):
    return make_response({'Message': 'Invalid Username or Password'}, 401)
  uuid = str(uuid4())
  sesh[user.username] = uuid
  res = make_response(jsonify(uuid), 200)
  return res


@login_routes.route('/auth/logout', methods=['POST'])
@cross_origin(origin="localhost", headers=['Content-Type', 'Authorization'])
def logout():
  json = request.get_json()
  user = session.query(User).filter(User.email == json['email']).first()
  if not user:
    return make_response({"Message": 'User does not exist'}, 404)
  if user.username in sesh:
    sesh.pop(user.username)
    return make_response({"Message": "Successful Logout"}, 200)
  return make_response({"Message": "No session by that user."})


@login_routes.route('/auth/auth_check', methods=['POST'])
@cross_origin(origin="localhost", headers=['Content-Type', 'Authorization'])
def check_auth():
  json = request.get_json()
  username = ''
  if json['cookie'] in sesh.values():
    for key, value in sesh.items():
      if value == json['cookie']:
        username = key
        break
    user = session.query(User).filter(User.username == username).first()
    res = make_response(jsonify({'username': user.username, 'email': None, 'password': None}), 200)
    return res
  return make_response({'Message': 'User not authed'}, 401)

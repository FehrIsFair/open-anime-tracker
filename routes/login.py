from flask import request, Blueprint, make_response
from flask import session as sesh
from flask_cors import cross_origin

from database import session
from db_models.users import User


login_routes = Blueprint('login', __name__)


@login_routes.route('/login', methods=['POST'])
@cross_origin(origin="localhost", headers=['Content-Type', 'Authorization'])
def login():
  from helper_funcs import bcrypt
  json = request.get_json()
  user = session.query(User).filter(User.email == json['email']).first()
  if not user:
    return make_response({'Message': 'Invalid Username or Password'}, 401)
  if user.id in sesh['uids']:
    return make_response({'Message': 'You are already logged in.'}, 200)
  if bcrypt.check_password_hash(json['password'], user.password):
    return make_response({'Message': 'Invalid Username or Password'}, 401)
  return make_response({'id': user.id, 'email': user.email}, 200)


@login_routes.route('/logout', methods=['POST'])
@cross_origin(origin="localhost", headers=['Content-Type', 'Authorization'])
def logout():
  json = request.get_json()
  if json['uid'] in sesh['uids']:
    sesh['uids'].remove(json['uid'])
    return make_response({"Message": "Successful Logout"}, 200)
  return make_response({"Message": "No session by that user."})

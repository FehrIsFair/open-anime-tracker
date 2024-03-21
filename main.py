from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import const
from flask_restful import Api

from routes.anime import anime_routes

db = SQLAlchemy()

app = Flask(__name__)
api = Api(app)
CORS(app, resource={r"/*": {"origins": "*"}})


app.config['SQLALCHEMY_DATABASE_URI'] = (f'postgresql://{const.PG_USER}:{const.PG_PW}@localhost:{const.PG_PORT}/db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['CORS_HEADERS'] = 'Content-Type'

# @app.before_request
# def cors_handling():
#   if request.method.lower() == 'options':
#     return Response()

@app.route('/')
def default():
  return "Hello World"

app.register_blueprint(anime_routes)

db.init_app(app)



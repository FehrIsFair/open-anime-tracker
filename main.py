import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import session
import const
from flask_restful import Api
from flask_session.redis import RedisSessionInterface
from redis import Redis

from config import ServerConfig
from routes.anime import anime_routes
from routes.login import login_routes
from routes.user import user_routes
from flask_bcrypt import Bcrypt

data_store_db_obj  = SQLAlchemy()

app = Flask(__name__)
api = Api(app)
CORS(app, resource={r"/*": {"origins": "*"}})
app.config.from_object(ServerConfig)
bcrypt = Bcrypt(app)

@app.route('/')
def default():
  return "Hello World"

app.register_blueprint(anime_routes)
app.register_blueprint(user_routes)
app.register_blueprint(login_routes)


if __name__ == '__main__':
  session['uids'] = []

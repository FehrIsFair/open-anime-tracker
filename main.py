
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_restful import Api
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from config import ServerConfig, _redis_valid
from routes.anime import anime_routes
from routes.kitsu import kitsu_routes
from routes.login import login_routes
from routes.user import user_routes

if not _redis_valid:
    print("\nFATAL: Redis is not available. Cannot start without session storage.\n")
    import sys

    sys.exit(1)

data_store_db_obj = SQLAlchemy()

app = Flask(__name__)
api = Api(app)
CORS(
    app,
    resources={
        r"/*": {"origins": "http://localhost:3000", "supports_credentials": True}
    },
)
app.config.from_object(ServerConfig)
bcrypt = Bcrypt(app)


@app.route("/")
def default():
    return "Hello World"


app.register_blueprint(anime_routes)
app.register_blueprint(kitsu_routes)
app.register_blueprint(user_routes)
app.register_blueprint(login_routes)

sesh = Session(app)

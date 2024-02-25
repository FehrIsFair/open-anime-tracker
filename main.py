from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import const


db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (f'postgresql://{const.PG_USER}:{const.PG_PW}@localhost:{const.PG_PORT}/db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

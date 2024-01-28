from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (f'postgres://{os.environ.get('POSTGRES_USER')}:'
                                         f'{os.environ.get('POSTGRES_PASSWORD')}@localhost:5432/db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

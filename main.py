from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import const

db = SQLAlchemy()

app = Flask(__name__)
cors = CORS(app, resource={r"/*": {"origins": "*"}})


app.config['SQLALCHEMY_DATABASE_URI'] = (f'postgresql://{const.PG_USER}:{const.PG_PW}@localhost:{const.PG_PORT}/db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

@app.before_request
def cors_handling():
  if request.method.lower() == 'options':
    return Response()

db.init_app(app)



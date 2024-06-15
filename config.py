import os

import redis

import const


class ServerConfig:
  SECRET_KEY = os.environ.get('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = (f'postgresql://{const.PG_USER}:{const.PG_PW}@localhost:{const.PG_PORT}/db')
  SQLALCHEMY_TRACK_MODIFICATIONS = True
  CORS_HEADERS = 'Content-Type'
  # enable session config
  SESSION_TYPE = "redis"
  # so that session won't be permenant
  SESSION_PERMANENT = False
  # use secret key signer
  SESSION_USE_SIGNER = True
  # set the path
  SESSION_REDIS = redis.from_url(f"redis://{const.REDIS_IP}:6379")


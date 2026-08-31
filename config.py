import os

from redis.client import Redis

import const


class ServerConfig:
  SECRET_KEY = os.environ.get('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = (f'postgresql://{const.PG_USER}:{const.PG_PW}@127.0.0.1:{const.PG_PORT}/db')
  SQLALCHEMY_TRACK_MODIFICATIONS = True
  CORS_HEADERS = 'Content-Type'
  # CORS will be configured per-resource in main.py with supports_credentials
  SESSION_TYPE = "redis"
  # so that session won't be permanent
  SESSION_PERMANENT = False
  # use secret key signer
  SESSION_USE_SIGNER = True
  # set the path
  SESSION_REDIS = Redis.from_url(f"redis://{const.REDIS_IP}:6379")


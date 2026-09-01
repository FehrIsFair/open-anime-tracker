import os

from redis.client import Redis

import const

# Build Redis URL defensively — if REDIS_IP is missing/empty, default to 127.0.0.1
_redis_ip = const.REDIS_IP or '127.0.0.1'
_redis_url = f"redis://{_redis_ip}:6379"

# Create the Redis client
_redis_client = Redis.from_url(_redis_url)

# Validate Redis connectivity at startup with clear diagnostic output
def _validate_redis_connection():
  try:
    _redis_client.ping()
    print(f"[config] Redis connected successfully at {_redis_url}")
    return True
  except Exception as e:
    import sys
    print(f"\n{'=' * 60}", file=sys.stderr)
    print(f"ERROR: Redis connection failed at startup!", file=sys.stderr)
    print(f"  URL: {_redis_url}", file=sys.stderr)
    print(f"  Error: {e}", file=sys.stderr)
    print(f"  Ensure Redis is running: docker compose up -d redis", file=sys.stderr)
    print(f"{'=' * 60}\n", file=sys.stderr)
    return False

_redis_valid = _validate_redis_connection()


class ServerConfig:
  SECRET_KEY = os.environ.get('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = (f'postgresql://{const.PG_USER}:{const.PG_PW}@127.0.0.1:{const.PG_PORT}/db')
  SQLALCHEMY_TRACK_MODIFICATIONS = True
  CORS_HEADERS = 'Content-Type'
  # CORS will be configured per-resource in main.py with supports_credentials
  SESSION_TYPE = "redis"
  SESSION_PERMANENT = False
  SESSION_KEY_PREFIX = 'flask_session:'
  # Cookie settings for cross-origin requests (localhost:3000 → localhost:5000)
  SESSION_COOKIE_DOMAIN = 'localhost'
  SESSION_COOKIE_SAMESITE = 'Lax'
  SESSION_COOKIE_HTTPONLY = True
  SESSION_REDIS = _redis_client


from dotenv import load_dotenv
import os
from requests import request

load_dotenv()

PG_USER = os.environ.get("POSTGRES_USER")
PG_PW = os.environ.get("POSTGRES_PASSWORD")
PG_PORT = os.environ.get("PG_PORT")
SALT = int(os.environ.get("SALT"))
REDIS_IP = os.environ.get("REDIS_IP")

kitsu_api_base = 'https://kitsu.io/api/edge'
kitsu_headers = {'Accept': 'application/vnd.api+json', 'Content-Type': 'application/vnd.api+json'}
c_id = ''
c_secret = ''

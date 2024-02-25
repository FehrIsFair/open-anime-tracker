from dotenv import load_dotenv
import os

load_dotenv()

PG_USER = os.environ.get("POSTGRES_USER")
PG_PW = os.environ.get("POSTGRES_PASSWORD")
PG_PORT = os.environ.get("PG_PORT")
SALT = os.environ.get("SALT")

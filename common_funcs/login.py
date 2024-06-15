import os


def valid_pw(pw: str, db_pw: str) -> bool:
  from helper_funcs import bcrypt
  hash = bcrypt.generate_password_hash(pw, os.environ.get('SALT')).decode('utf-8')
  if hash == db_pw:
    return True
  return False

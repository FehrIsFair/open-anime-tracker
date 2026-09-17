import flask_bcrypt


def valid_pw(pw: str, db_pw: str) -> bool:
  return flask_bcrypt.check_password_hash(pw.encode('utf-8'), db_pw)
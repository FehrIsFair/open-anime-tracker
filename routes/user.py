import datetime
from datetime import UTC

import flask_bcrypt
from flask import Blueprint, make_response, request
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

from database import session
from db_models.users import User

user_routes = Blueprint("user", __name__)


@user_routes.route("/user", methods=["GET"])
def index():
    return_list = []
    try:
        req_user = session.query(User).all()
    except SQLAlchemyError as e:
        print(e)
        return make_response({"Message": "Could not find users"}, 500)

    return_list = [u.make_json() for u in req_user]

    return make_response({"data": return_list}, 200)


@user_routes.route("/user/create", methods=["POST"])
def create_user():
    json = request.get_json()
    user = (
        session.query(User)
        .filter(and_(User.email == json["email"], User.username == json["username"]))
        .first()
    )

    if user:
        return make_response(
            {"Message": "User already exists with email, username combo"}, 409
        )
    hash_ = flask_bcrypt.generate_password_hash(
        json["password"].encode("utf-8")
    ).decode("utf-8")

    new_user = User(json["email"], hash_, json["username"])

    try:
        session.add(new_user)
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        return make_response({"Message": "Could not create new user"}, 500)

    return make_response({"Message": "User create successfully"}, 200)


@user_routes.route("/user/update_pw", methods=["PATCH"])
def update_password():
    json = request.get_json()
    user = session.query(User).filter(and_(User.id == json["id"])).first()

    if not user:
        return make_response({"Message": "User not found"}, 500)

    if not flask_bcrypt.check_password_hash(
        json["old_password"].encode("utf-8"), user.password.encode("utf-8")
    ):
        return make_response({"Message": "Old password did not match."}, 500)

    new_hash = flask_bcrypt.generate_password_hash(
        json["new_password"].encode("utf-8")
    ).decode("utf-8")
    user.password = new_hash

    try:
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        return make_response({"Message": "Could not update password"}, 500)
    return make_response({"Message": "Password updated"}, 200)


@user_routes.route("/user/edit", methods=["PATCH"])
def edit_user():
    json = request.get_json()
    user = session.query(User).filter(and_(User.id == json["id"])).first()

    if not user:
        return make_response({"Message": "User not found"}, 404)

    if "password" in json and not flask_bcrypt.checkpw(
        json["password"].encode("utf-8"), user.password.encode("utf-8")
    ):
        return make_response(
            {"Message": "Password did not match, will not update user"}, 500
        )

    kwargs = {}
    for key, value in json.items():
        if key != "password":
            kwargs[key] = value

    user.set_values(**kwargs)

    try:
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        return make_response({"Message": "User could not be updated"}, 500)
    return make_response({"Message": "User updated."}, 200)


@user_routes.route("/user/delete", methods=["DELETE"])
def delete_user():
    json = request.get_json()
    user = session.query(User).filter(and_(User.id == json["id"])).first()

    if not user:
        return make_response({"Message": "User not found"}, 404)

    user.deleted_at = datetime.datetime.now(tz=UTC)

    try:
        session.commit()
    except SQLAlchemyError as e:
        print(e)
        session.rollback()
        return make_response({"Message": "Could not delete user"}, 500)

    return make_response({"Message": "User Successfully deleted"}, 200)

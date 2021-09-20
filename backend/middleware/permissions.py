from functools import wraps
from flask import abort, make_response, jsonify
from flask.wrappers import Response
from flask_jwt_extended import get_jwt
from ..models.CraneUser import CraneUser, UserCatgoryEnum

# data admin
# applicatio admin

def only_application_admin(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        current_user_email = get_jwt()
        user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()
        if user.UserCategory != UserCatgoryEnum.App_Admin:
            return make_response(jsonify({'message':"You don't have permission to carryout this request"}),403)
        return function(*args, **kwargs)
    return wrapper


def only_data_admin(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        current_user_email = get_jwt()
        user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()
        if user.UserCategory != UserCatgoryEnum.Data_Admin:
            return make_response(jsonify({'message':"You don't have permission to carryout this request"}),403)
            # abort(403, Response("You don't have permission to carryout this request"))
        return function(*args, **kwargs)
    return wrapper


def only_application_and_data_admin(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        current_user_email = get_jwt()
        user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()
        if user.UserCategory != UserCatgoryEnum.App_Admin or user.UserCategory != UserCatgoryEnum.App_Admin:
            return make_response(jsonify({'message':"You don't have permission to carryout this request"}),403)
        return function(*args, **kwargs)
    return wrapper



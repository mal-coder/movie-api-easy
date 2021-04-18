"""
Module containing decorator function responsible for authenticating the provided token
"""

from flask_restful import abort

from app.config import api_key


def authenticate_token(func, *args):
    def wrapper(req_parameter, req_token, *args):
        split_token = req_token.split()
        if len(split_token) != 2 or split_token[0].lower() != 'bearer':
            abort(400, message='Authorization header missing or token in incorrect format')
        elif split_token[1] != api_key:
            abort(401, message='Authorization token is incorrect')
        return func(*args, req_parameter)

    return wrapper

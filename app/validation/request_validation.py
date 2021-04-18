"""
Module containing decorator function responsible for validating request's
Authorization header and query parameter
"""

from flask import request
from flask_restful import abort

from app.config import parameter


def validate_request(func):
    def wrapper(*args):
        # Retrieve Authorization header and query parameter
        req_token = request.headers.get('Authorization').strip()
        req_parameter = request.args.get(parameter)
        # Clean from trailing and leading blanks
        req_token = req_token.strip() if req_token else req_token
        req_parameter = req_parameter.strip() if req_parameter else req_parameter
        # If any is missing throw Bad Request error
        if not req_token:
            abort(400, message=f"Required 'Authorization' header is missing or empty")
        if not req_parameter:
            abort(400, message=f"Required query parameter '{parameter}' is missing or empty")

        return func(req_parameter, req_token, *args)

    return wrapper

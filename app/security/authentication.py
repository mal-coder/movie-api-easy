from flask_restful import abort

from app.config import api_key
from app.validation.request_parser import parser


def authenticate_token(func):
    def wrapper(*args, **kwargs):
        token = parser.parse_args().get('Authorization')
        split_token = token.split()
        if not token or len(split_token) != 2 or split_token[0].lower() != 'bearer':
            abort(400, message='Authorization header missing or token in incorrect format')
        elif split_token[1] != api_key:
            abort(401, message='Authorization token is incorrect')
        return func(*args, **kwargs)

    return wrapper

from flask_restful import reqparse

from app.config import parameter

parser = reqparse.RequestParser()
parser.add_argument(parameter, type=str, location='args', required=True)
parser.add_argument('Authorization', type=str, location='headers', required=True)

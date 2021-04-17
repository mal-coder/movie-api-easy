from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, location='args', required=True)
parser.add_argument('Authorization', type=str, location='headers', required=False)

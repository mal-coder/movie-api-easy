from flask import Flask
from flask_restful import Api

from app.resources.movie import MovieEndpoint


def get_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(MovieEndpoint, '/')

    return app

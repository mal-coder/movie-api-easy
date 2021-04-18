"""
Module containing application's creation logic
"""

from flask import Flask
from flask_restful import Api

from app.resources.movie import MovieEndpoint


def get_app():
    # Create flask instance
    app = Flask(__name__)
    api = Api(app)
    # Add routes/resources
    api.add_resource(MovieEndpoint, '/')

    return app

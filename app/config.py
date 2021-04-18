"""
Module containing retrieved environmental variables and default configuration
"""

import json
from os import environ

xml_api_uri = environ['XML_API_URI']
api_key = environ['API_KEY']
xml_query_parameter = environ.get('XML_QUERY_PARAMETER', 't')
xml_attributes = json.loads(environ.get('XML_ATTRIBUTES',
                                        '["title", "year", "rated", "released", "runtime", "genre", "director", "writer", "actors", "plot", "language", "country", "awards", "poster", "metascore", "imdbRating", "imdbVotes", "imdbID", "type"]'))
port = environ.get('PORT', '5000')
host = environ.get('HOST', '0.0.0.0')
parameter = environ.get('QUERY_PARAMETER', 'title')
painless = False

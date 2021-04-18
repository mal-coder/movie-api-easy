"""
Module containing API's MovieEndpoint Resource.
Resource in Flask RESTful has te same role as "route" in different frameworks/naming conventions.
It handles the logic of retrieving data from the target server, converting it to the desired format and
returning to the client.

TODO
If the logic will be extending move it to separate functions
"""

import logging
from urllib.error import URLError
from urllib.request import urlopen
from xml.etree import ElementTree

from flask_restful import Resource, abort
from werkzeug.exceptions import NotFound, BadRequest

from app.config import xml_api_uri, xml_attributes, painless, xml_query_parameter
from app.security.authentication import authenticate_token
from app.validation.request_validation import validate_request


class MovieEndpoint(Resource):
    @validate_request
    @authenticate_token
    def get(self, req_parameter):
        try:
            # Prepare request url and retrieve data from target server
            url = f'{xml_api_uri}&{xml_query_parameter}={req_parameter}'
            with urlopen(url) as request:
                response = request.read()

            # Parse retrieved data
            # Using xml.etree
            if painless:
                xml_response = ElementTree.fromstring(response)
                for child in xml_response:
                    if child.text == 'Movie not found!':
                        abort(404, message=child.text)
                    elif child.tag == 'movie':
                        return child.attrib
            # Using manual parsing
            else:
                content = str(response, 'utf-8')
                if '<error>Movie not found!</error>' in content:
                    abort(404, message='Movie not found!')
                elif '<error>Incorrect IMDb ID.</error>' in content:
                    abort(400, message='Incorrect IMDb ID.')
                movie_data = dict()
                for attr in xml_attributes:
                    attr_lindex = content.find(attr)
                    vale_lindex = attr_lindex + len(attr) + len('="')
                    value_rindex = vale_lindex + content[vale_lindex:].find('"')
                    movie_data[attr] = content[vale_lindex:value_rindex]
                return movie_data

        except URLError:
            logging.exception("Error while processing the request")
            message = "Error while processing request"
            abort(500, message=message)
        except NotFound:
            raise
        except BadRequest:
            raise
        except Exception:
            logging.exception("Error while processing request")
            abort(500, message=f'Unknown server error')

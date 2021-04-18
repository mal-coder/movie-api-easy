import logging
from urllib.request import urlopen
from http.client import HTTPException
from xml.etree import ElementTree

from flask_restful import Resource, abort
from werkzeug.exceptions import NotFound

from app.config import xml_api_uri, xml_attributes, painless, parameter, xml_query_parameter
from app.security.authentication import authenticate_token
from app.validation.request_parser import parser


class MovieEndpoint(Resource):
    @authenticate_token
    def get(self):
        title = parser.parse_args().get(parameter, None)
        try:
            url = f'{xml_api_uri}&{xml_query_parameter}={title}'
            with urlopen(url) as request:
                response = request.read()

            if painless:
                xml_response = ElementTree.fromstring(response)
                for child in xml_response:
                    if child.text == 'Movie not found!':
                        abort(404, message=child.text)
                    elif child.tag == 'movie':
                        return child.attrib
            else:
                content = str(response, 'utf-8')
                if '<error>Movie not found!</error>' in content:
                    abort(404, message='Movie not found!')
                movie_data = dict()
                for attr in xml_attributes:
                    attr_lindex = content.find(attr)
                    vale_lindex = attr_lindex + len(attr) + len('="')
                    value_rindex = vale_lindex + content[vale_lindex:].find('"')
                    movie_data[attr] = content[vale_lindex:value_rindex]
                return movie_data

        except HTTPException:
            logging.exception("Error while processing request")
            message = "Error while processing request"
            abort(500, message=message)
        except NotFound:
            raise
        except Exception:
            logging.exception("Error while processing request")
            abort(500, message=f'Unknown server error')

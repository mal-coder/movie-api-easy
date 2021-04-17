import logging
from xml.etree import ElementTree

import requests
from flask_restful import Resource, abort

from app.config import xml_api_uri, xml_attributes, painless, parameter
from app.security.authentication import authenticate_token
from app.validation.request_parser import parser


class MovieEndpoint(Resource):
    @authenticate_token
    def get(self):
        title = parser.parse_args().get(parameter, None)
        try:
            url = f'{xml_api_uri}&t={title}'
            response = requests.get(url)
            response.raise_for_status()

            if painless:
                xml_response = ElementTree.fromstring(response.content)
                for child in xml_response:
                    if child.text == 'Movie not found!':
                        abort(404, message=child.text)
                    elif child.tag == 'movie':
                        return child.attrib
            else:
                content = response.text
                movie_data = dict()
                for attr in xml_attributes:
                    attr_lindex = content.find(attr)
                    vale_lindex = attr_lindex + len(attr) + len('="')
                    value_rindex = vale_lindex + content[vale_lindex:].find('"')
                    movie_data[attr] = content[vale_lindex:value_rindex]
                return movie_data

        except requests.HTTPError:
            logging.exception("Error while processing request")
            message = "Error while processing request"
            if response.text:
                message = response.text
            abort(500, message=message)
        except Exception:
            logging.exception("Error while processing request")
            abort(500, message=f'Unknown server error')

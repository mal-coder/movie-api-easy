import json
from os import environ

painless = False
xml_api_uri = environ['XML_API_URI']
api_key = environ['API_KEY']
xml_attributes = json.loads(environ['XML_ATTRIBUTES'])
port = environ['PORT']
host = environ['HOST']
parameter = environ.get('QUERY_PARAMETER', 'title')

import pytest
from flask import json

from app.config import api_key, parameter
from run import application


@pytest.fixture
def client():
    application.config['TESTING'] = True
    with application.test_client() as client:
        yield client


def test_validation_token_unauthorized(client):
    headers = {'Authorization': f'Bearer wrong-token'}
    query_parameters = f'?{parameter}=Lost'
    path = '/'
    response = client.get(path=path + query_parameters, headers=headers)

    assert response.status_code == 401


def test_validation_bearer_key_missing(client):
    headers = {'Authorization': f'Not-Bearer wrong-token'}
    query_parameters = f'?{parameter}=Lost'
    path = '/'
    response = client.get(path=path + query_parameters, headers=headers)

    assert response.status_code == 400
    assert b'Authorization header missing or token in incorrect format' in response.data


def test_validation_query_parameter_missing(client):
    headers = {'Authorization': f'Bearer {api_key}'}
    path = '/'

    response = client.get(path=path, headers=headers)

    assert response.status_code == 400
    assert b'Missing required parameter in the query string' in response.data


def test_get_movie_success(client):
    headers = {'Authorization': f'Bearer {api_key}'}
    query_parameters = f'?{parameter}=Lost'
    path = '/'
    response = client.get(path=path + query_parameters, headers=headers)

    data_json = json.loads(response.data)

    assert data_json['country'] == 'USA'
    assert response.status_code == 200


def test_get_movie_not_found(client):
    headers = {'Authorization': f'Bearer {api_key}'}
    query_parameters = f'?{parameter}=aaabbbssss'
    path = '/'
    response = client.get(path=path + query_parameters, headers=headers)

    assert response.status_code == 404

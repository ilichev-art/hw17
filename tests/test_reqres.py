import json
import requests
from jsonschema import validate
from utils.path import schema_path



def test_post_create_user(base_url):
    payload = {'name': 'morpheus', 'job': 'leader'}

    response = requests.post(base_url + '/users', data=payload)
    body = response.json()

    assert response.status_code == 201
    schema = schema_path("users.json")
    with open(schema) as file:
        validate(body, schema=json.loads(file.read()))


def test_post_name_returns(base_url):
    name = 'Anna'
    job = 'CTO'

    response = requests.post(base_url + '/users', data={"name": name, "job": job})
    body = response.json()

    assert response.status_code == 201
    assert body['name'] == name


def test_get_single_user_by_id(base_url):
    id = '2'
    response = requests.get(base_url + '/users/' + id)
    body = response.json()

    assert body['data']['id'] == int(id)
    assert response.status_code == 200
    schema = schema_path("single_user.json")
    with open(schema) as file:
        validate(body, schema=json.loads(file.read()))


def test_put_update_last_name(base_url):
    id = '2'
    last_name = 'Robbie'

    response = requests.put(base_url + '/users/' + id, data={"last_name": last_name})
    boby = response.json()

    assert response.status_code == 200
    assert boby['last_name'] == last_name


def test_get_user_not_found(base_url):
    id = '23'
    response = requests.get(base_url + '/users/' + id)

    assert response.status_code == 404
    assert response.text == '{}'


def test_delete_user(base_url):
    id = '2'
    response = requests.delete(base_url + '/users/' + id)

    assert response.status_code == 204
    assert response.text == ''


def test_get_delay_response(base_url):
    endpoint = '/users?delay=3'
    response = requests.get(base_url + endpoint)
    body = response.json()

    assert response.status_code == 200
    assert response.elapsed.total_seconds() <= 3.500000
    schema = schema_path('users_with_delay.json')
    with open(schema) as file:
        validate(body, schema=json.loads(file.read()))


def test_post_register_unsuccessful(base_url):
    payload = {'email': "sydney@fife"}
    response = requests.post(base_url + '/register', data=payload)

    assert response.status_code == 400
    assert response.json() == {"error": "Missing password"}
    schema = schema_path("missing_password.json")
    with open(schema) as file:
        validate(response.json(), schema=json.loads(file.read()))

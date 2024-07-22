import json
import requests
from jsonschema import validate
from pathlib import Path

def schema_path(name):
    return str(Path(__file__).parent.parent.joinpath(f'schemas/{name}'))

url = 'https://reqres.in/api'


# positive tests
def test_post_create_user():
    payload = {'name': 'morpheus', 'job': 'leader'}

    response = requests.post(f'{url}/users', data=payload)
    body = response.json()

    assert response.status_code == 201
    schema = schema_path("users.json")
    with open(schema) as file:
      validate(body, schema=json.loads(file.read()))


def test_post_name_returns():
    name = 'Anna'
    job = 'CTO'

    response = requests.post(f'{url}/users', data={"name": name,"job": job})
    body = response.json()

    assert response.status_code == 201
    assert body['name'] == name

def test_get_single_user_by_id():
    id = '2'
    response = requests.get(f'{url}/users/{id}')
    body = response.json()

    assert body['data']['id'] == int(id)
    assert response.status_code == 200
    schema = schema_path("single_user.json")
    with open(schema) as file:
        validate(body, schema=json.loads(file.read()))

def test_put_update_last_name():
    last_name = 'Robbie'

    response = requests.put(f'{url}/users/2', data={"last_name": last_name})
    boby = response.json()

    assert response.status_code == 200
    assert boby['last_name'] == last_name

def test_get_user_not_found():
    id = '23'
    response = requests.get(f'{url}/users/{id}')

    assert response.status_code == 404
    assert response.text == '{}'

def test_delete_user():
    response = requests.delete(f'{url}/users/2')

    assert response.status_code == 204
    assert response.text == ''

def test_get_delay_response():
    endpoint = '/users?delay=3'
    response = requests.get(url + endpoint)
    body = response.json()

    assert response.status_code == 200
    assert response.elapsed.total_seconds() <= 3.500000
    schema = schema_path('users_with_delay.json')
    with open(schema) as file:
        validate(body, schema=json.loads(file.read()))

def test_post_register_unsuccessful():
    payload = {'email': "sydney@fife"}
    response = requests.post(f'{url}/register', data=payload)

    assert response.status_code == 400
    assert response.json() == {"error": "Missing password"}
    schema = schema_path("missing_password.json")
    with open(schema) as file:
        validate(response.json(), schema=json.loads(file.read()))





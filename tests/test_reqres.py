import json
import requests
from jsonschema import validate
from pathlib import Path

def schema_path(name):
    return str(Path(__file__).parent.parent.joinpath(f'schemas/{name}'))

def test_create_user():
    name = 'morpheus'
    job = 'leader'

    response = requests.post('https://reqres.in/api/users', data={"name": name, "job": job})
    body = response.json()

    assert response.status_code == 201
    schema = schema_path("users.json")
    with open(schema) as file:
      validate(body, schema=json.loads(file.read()))


def test_name_returns():
    name = 'Anna'
    job = 'CTO'

    response = requests.post('https://reqres.in/api/users', data={"name": name,"job": job})
    body = response.json()

    assert response.status_code == 201
    assert body['name'] == name
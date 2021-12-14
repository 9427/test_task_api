import pytest
import requests

API_ROUTE = 'http://backend:5000/api/v1/employees'
DEFAULT_VALS = {
    'lastname': 'Pupkin',
    'firstname': 'Vasya',
    'patronym': 'Ivanovich',
    'birthyear': 1994,
    'id': 1234,
    'salary': 250000,
    'jobname': 'Senior Pomidor Developer',
    'company': 'RedApple',
    'department': 'Pomidor Team'
}


@pytest.fixture
def increment_id():
    DEFAULT_VALS['id'] += 1
    return DEFAULT_VALS


def request(method, params=None, route_id=0, timeout=5):
    if route_id:
        route = API_ROUTE + '/' + str(route_id)
    else:
        route = API_ROUTE
    if method == 'GET':
        response = requests.get(route, params=params, timeout=timeout)
    elif method == 'POST':
        response = requests.post(route, params=params, timeout=timeout)
    elif method == 'PATCH':
        response = requests.patch(route, params=params, timeout=timeout)
    elif method == 'DELETE':
        response = requests.delete(route, params=params, timeout=timeout)
    return response

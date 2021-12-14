from helpers import request, DEFAULT_VALS, increment_id


def test_read_all():
    response = request('GET')
    assert response.json()['result']
    assert response.status_code == 200


def test_add_employee(increment_id):
    response = request('POST', DEFAULT_VALS)
    assert response.status_code == 201


def test_search_employee(increment_id):
    request('POST', DEFAULT_VALS)
    response = request('GET', DEFAULT_VALS)
    assert response.json()['result'][0]['jobname'] == DEFAULT_VALS['jobname']
    assert response.status_code == 200


def test_update_employee(increment_id):
    request('POST', DEFAULT_VALS)
    new_salary = DEFAULT_VALS['salary'] + 100000
    request('PATCH', {'salary': new_salary}, route_id=DEFAULT_VALS['id'])
    response = request('GET', {'id': DEFAULT_VALS['id']})
    assert response.json()['result'][0]['salary'] == new_salary
    assert response.status_code == 200


def test_delete_employee(increment_id):
    request('POST', DEFAULT_VALS)
    response = request('DELETE', route_id=DEFAULT_VALS['id'])
    assert response.status_code == 204
    response = request('GET', {'id': DEFAULT_VALS['id']})
    assert response.json()['error']
    assert response.status_code == 404

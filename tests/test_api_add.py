from helpers import request, DEFAULT_VALS, increment_id

METHOD = '/add'


def test_add_employee_correct(increment_id):
    request('POST', DEFAULT_VALS)
    response = request('GET', DEFAULT_VALS)
    assert response.json()['result']
    for key in response.json()['result'][0]:
        assert key in DEFAULT_VALS.keys()
        assert response.json()['result'][0][key] in DEFAULT_VALS.values()


def test_add_employee_missing_vals(increment_id):
    query_vals = DEFAULT_VALS.copy()
    query_vals.pop('firstname')
    query_vals.pop('salary')
    response = request('POST', query_vals)
    assert response.json()['error']


def test_add_employee_existing_id(increment_id):
    request('POST', DEFAULT_VALS)
    response = request('POST', DEFAULT_VALS)
    assert response.json()['error']


def test_add_employee_wrong_data_type_1(increment_id):
    query_vals = DEFAULT_VALS.copy()
    query_vals['salary'] = 'Mnogo'
    response = request('POST', query_vals)
    assert response.json()['error']


def test_add_employee_wrong_data_type_2(increment_id):
    query_vals = DEFAULT_VALS.copy()
    query_vals['birthyear'] = 'Davno'
    response = request('POST', query_vals)
    assert response.json()['error']
    

def test_add_employee_wrong_data_type_3(increment_id):
    query_vals = DEFAULT_VALS.copy()
    query_vals['id'] = 12345.67
    response = request('GET', query_vals)
    assert response.json()['error']

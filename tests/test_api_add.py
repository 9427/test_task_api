from helpers import get, create_query, DEFAULT_VALS

METHOD = '/add'


def test_add_employee_correct():
    DEFAULT_VALS['id'] += 1
    query = create_query(DEFAULT_VALS)
    get(METHOD + query)
    response = get(query)
    assert response['result']
    for key in response['result'][0]:
        assert key in DEFAULT_VALS.keys()
        assert response['result'][0][key] in DEFAULT_VALS.values()


def test_add_employee_missing_vals():
    DEFAULT_VALS['id'] += 1
    query_vals = DEFAULT_VALS.copy()
    query_vals.pop('firstname')
    query_vals.pop('salary')
    query = create_query(query_vals)
    response = get(METHOD + query)
    assert response['error']


def test_add_employee_existing_id():
    DEFAULT_VALS['id'] += 1
    query = create_query(DEFAULT_VALS)
    get(METHOD + query)
    response = get(METHOD + query)
    assert response['error']


def test_add_employee_wrong_data_type_1():
    DEFAULT_VALS['id'] += 1
    query_vals = DEFAULT_VALS.copy()
    query_vals['salary'] = 'Mnogo'
    query = create_query(query_vals)
    response = get(METHOD + query)
    assert response['error']


def test_add_employee_wrong_data_type_2():
    DEFAULT_VALS['id'] += 1
    query_vals = DEFAULT_VALS.copy()
    query_vals['birthyear'] = 'Davno'
    query = create_query(query_vals)
    response = get(METHOD + query)
    assert response['error']
    

def test_add_employee_wrong_data_type_3():
    DEFAULT_VALS['id'] += 1
    query_vals = DEFAULT_VALS.copy()
    query_vals['id'] = 12345.67
    query = create_query(query_vals)
    response = get(METHOD + query)
    assert response['error']

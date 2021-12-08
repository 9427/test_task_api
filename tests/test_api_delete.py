from helpers import get, create_query, DEFAULT_VALS

METHOD = '/delete'


def test_delete_empty_query():
    response = get(METHOD)
    assert response['error']


def test_delete_missing_entry():
    response = get(METHOD, create_query({'id': 98765}))
    assert response['error']


def test_delete_multiple_employees():
    # should return error!
    query_vals = DEFAULT_VALS.copy()
    query_vals['lastname'] = 'Foobar'
    n = 3
    for i in range(n):
        query_vals['id'] += 1
        get('/add' + create_query(query_vals))
    DEFAULT_VALS['id'] += 3
    response = get(METHOD + create_query({'lastname': query_vals['lastname']}))
    assert response['error']
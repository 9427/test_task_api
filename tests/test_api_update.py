from helpers import get, create_query, DEFAULT_VALS

METHOD = '/update'


def test_update_no_search_id():
    query = create_query(DEFAULT_VALS)
    response = get(METHOD + query)
    assert response['error']


def test_update_wrong_type():
    DEFAULT_VALS['id'] += 1
    get('/add' + create_query(DEFAULT_VALS))
    query_vals = DEFAULT_VALS.copy()
    query_vals['search_id'] = DEFAULT_VALS['id']
    query_vals['salary'] = 'Mnogo'
    response = get(METHOD + create_query(query_vals))
    assert response['error']


def test_update_missing_entry():
    query_vals = DEFAULT_VALS.copy()
    query_vals['search_id'] = 98765
    query_vals['salary'] += 50000
    response = get(METHOD + create_query(query_vals))
    assert response['error']


def test_update_no_changes():
    DEFAULT_VALS['id'] += 1
    query_vals = DEFAULT_VALS.copy()
    print(get('/add' + create_query(query_vals)))
    query_vals['search_id'] = query_vals['id']
    print(get(METHOD + create_query(query_vals)))
    print(create_query({'id': query_vals['id']}))
    response = get(create_query({'id': query_vals['id']}))
    print(response)
    assert response['result']
    for key in response['result'][0]:
        assert key in query_vals.keys()
        assert response['result'][0][key] in query_vals.values()

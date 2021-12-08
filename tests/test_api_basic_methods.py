from helpers import get, create_query, DEFAULT_VALS


def test_read_all():
    response = get('/all')
    assert response['result']


def test_add_employee():
    DEFAULT_VALS['id'] += 1
    response = get('/add' + create_query(DEFAULT_VALS))
    assert response['result']


def test_search_employee():
    DEFAULT_VALS['id'] += 1
    get('/add' + create_query(DEFAULT_VALS))
    response = get(create_query(DEFAULT_VALS))
    assert response['result'][0]['jobname'] == DEFAULT_VALS['jobname']


def test_update_employee():
    DEFAULT_VALS['id'] += 1
    get('/add' + create_query(DEFAULT_VALS))
    query_vals = {'search_id': DEFAULT_VALS['id'], 'salary': 180000}
    get('/update' + create_query(query_vals))
    query_vals = {'id': DEFAULT_VALS['id']}
    response = get(create_query(query_vals))
    assert response['result'][0]['salary'] == 180000


def test_delete_employee():
    DEFAULT_VALS['id'] += 1
    print(get('/add' + create_query(DEFAULT_VALS)))
    response = get('/delete' + create_query(DEFAULT_VALS))
    print(response)
    assert response['result']
    response = get(create_query(DEFAULT_VALS))
    assert response['error']

from helpers import get, create_query, DEFAULT_VALS


def test_search_wrong_filter_type():
    query_vals = {'firstname': 'Vasya', 'lastname': 'Pupkin', 'id': 'foobar'}
    response = get(create_query(query_vals))
    assert response['error']


def test_search_no_valid_filters():
    query_vals = {'salary': 60000, 'foo': 2.57, 'bar': 'yes'}
    response = get(create_query(query_vals))
    assert response['error']


def test_search_multiple_results():
    query_vals = DEFAULT_VALS.copy()
    query_vals['patronym'] = 'Foobarovich'
    method = '/add'
    n = 5
    for i in range(n):
        query_vals['id'] += 1
        print(get(method + create_query(query_vals)))
    DEFAULT_VALS['id'] += n
    query_vals = {'patronym': 'Foobarovich'}
    response = get(create_query(query_vals))
    assert len(response['result']) == n

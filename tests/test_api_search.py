from helpers import DEFAULT_VALS, request


def test_search_wrong_filter_type():
    query_vals = {'firstname': 'Vasya', 'lastname': 'Pupkin', 'id': 'foobar'}
    response = request('GET', query_vals)
    assert response.json()['error']
    assert response.status_code == 400


def test_search_no_valid_filters():
    query_vals = {'salary': 60000, 'foo': 2.57, 'bar': 'yes'}
    response = request('GET', query_vals)
    assert response.json()['error']
    assert response.status_code == 400


def test_search_multiple_results():
    query_vals = DEFAULT_VALS.copy()
    query_vals['patronym'] = 'Foobarovich'
    n = 5
    for i in range(n):
        query_vals['id'] += 1
        print(request('POST', query_vals))
    DEFAULT_VALS['id'] += n
    response = request('GET', {'patronym': 'Foobarovich'})
    assert response.status_code == 200
    assert len(response.json()['result']) == n

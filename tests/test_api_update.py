from helpers import DEFAULT_VALS, request, increment_id


def test_update_no_search_id():
    response = request('PATCH')
    assert response.json()['error']
    assert response.status_code == 405


def test_update_wrong_type(increment_id):
    request('POST', DEFAULT_VALS)
    response = request('PATCH', {'salary': 'Mnogo'}, DEFAULT_VALS['id'])
    assert response.json()['error']
    assert response.status_code == 400


def test_update_missing_entry():
    response = request('PATCH', {'salary': 50000}, 98765)
    assert response.json()['error']
    assert response.status_code == 404


def test_update_no_changes(increment_id):
    request('POST', DEFAULT_VALS)
    request('PATCH', route_id=DEFAULT_VALS['id'])
    response = request('GET', {'id': DEFAULT_VALS['id']})
    assert response.status_code == 200
    assert response.json()['result']
    for key in response.json()['result'][0]:
        assert key in DEFAULT_VALS.keys()
        assert response.json()['result'][0][key] in DEFAULT_VALS.values()



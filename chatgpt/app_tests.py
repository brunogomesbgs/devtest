def test_create_demand(client):
    response = client.post('/demand', json={'floor_origin': 0, 'floor_destiny': 10})
    assert response.status_code == 201
    assert response.get_json() == {'message': 'Demand created'}


def test_create_state(client):
    response = client.post('/state', json={'floor': 5, 'vacant': True})
    assert response.status_code == 201
    assert response.get_json() == {'message': 'State created'}


def test_get_prediction_floor(client):
    response = client.get('/prediction', json={})
    assert response.status_code == 200
    assert response.json['data']['floor'] == 0
    assert response.json['data']['qtt'] >= 1

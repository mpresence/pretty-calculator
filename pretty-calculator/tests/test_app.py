import pytest
from calculator import app as flask_app
import json

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Pretty Calculator' in response.data

def test_calculate_route_addition(client):
    response = client.post('/calculate', 
                         data=json.dumps({'expression': '2+3'}),
                         content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['result'] == 5

def test_calculate_route_subtraction(client):
    response = client.post('/calculate', 
                         data=json.dumps({'expression': '10-4'}),
                         content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['result'] == 6

def test_calculate_route_multiplication(client):
    response = client.post('/calculate', 
                         data=json.dumps({'expression': '5*6'}),
                         content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['result'] == 30

def test_calculate_route_division(client):
    response = client.post('/calculate', 
                         data=json.dumps({'expression': '15/3'}),
                         content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['result'] == 5

def test_calculate_route_complex_expression(client):
    response = client.post('/calculate', 
                         data=json.dumps({'expression': '(2+3)*4-6/2'}),
                         content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['result'] == 17

def test_calculate_route_scientific_function(client):
    response = client.post('/calculate', 
                         data=json.dumps({'expression': 'sqrt(16)'}),
                         content_type='application/json')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['result'] == 4

def test_calculate_route_error_handling(client):
    response = client.post('/calculate', 
                         data=json.dumps({'expression': '1/0'}),
                         content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_calculate_route_invalid_expression(client):
    response = client.post('/calculate', 
                         data=json.dumps({'expression': 'invalid'}),
                         content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
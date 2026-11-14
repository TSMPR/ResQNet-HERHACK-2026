from fastapi.testclient import TestClient
from backend.app import app
client = TestClient(app)

def test_health():
    assert client.get('/health').status_code == 200

def test_create_report():
    r = client.post('/api/v1/reports', json={'text':'Water has entered houses after heavy rain','language':'en'})
    assert r.status_code == 200
    assert 'prediction' in r.json()

def test_nearby_demo_resources():
    r = client.get('/api/v1/resources/nearby', params={'latitude':17.385,'longitude':78.4867,'radius_km':10})
    assert r.status_code == 200
    assert 'warning' in r.json()

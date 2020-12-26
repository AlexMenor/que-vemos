from app.app import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_status():
    response = client.get("/status")
    body = response.json()

    assert response.status_code == 200
    assert body['status'] == 'OK'

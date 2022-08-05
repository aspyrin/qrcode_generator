from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "QR Code Generator"}


data = {
    "url": "http://localhost:8000/tratata"
}


def test_qr_code():
    response = client.post('/qr-code', json=data)
    assert response.status_code == 200
    assert response.headers['content-type'] == 'image/png'
    assert int(response.headers["content-length"]) > 0

from http import HTTPStatus
from src.app import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_health_check_v1():
    """
    Testa a rota de health check da versão 1.
    """
    response = client.get("/api/v1/health")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "healthy"}

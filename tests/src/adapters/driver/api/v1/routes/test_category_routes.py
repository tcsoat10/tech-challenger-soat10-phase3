from http import HTTPStatus

import pytest

@pytest.mark.parametrize("payload", [
    {"name": "Drinks", "description": "Beverages category"},
    {"name": "Burgers", "description": "Fast food category"},
])
def test_create_category_success(client, payload):
    response = client.post("/api/v1/categories", json=payload)

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert "id" in data
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]

def test_create_category_duplicate_name_and_return_error(client):
    payload = {"name": "Drinks", "description": "Beverages category"}
    response = client.post("/api/v1/categories", json=payload)

    assert response.status_code == HTTPStatus.CREATED

    response = client.post("/api/v1/categories", json=payload)

    assert response.status_code == HTTPStatus.CONFLICT

    data = response.json()

    assert data == {'error': 'Category already exists.'}

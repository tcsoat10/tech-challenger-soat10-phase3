from fastapi import status

import pytest

@pytest.mark.parametrize("payload", [
    {"name": "Drinks", "description": "Beverages category"},
    {"name": "Burgers", "description": "Fast food category"},
])
def test_create_category_success(client, payload):
    response = client.post("/api/v1/categories", json=payload)

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert "id" in data
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]

def test_create_category_duplicate_name_and_return_error(client):
    payload = {"name": "Drinks", "description": "Beverages category"}
    response = client.post("/api/v1/categories", json=payload)

    assert response.status_code == status.HTTP_201_CREATED

    response = client.post("/api/v1/categories", json=payload)

    assert response.status_code == status.HTTP_409_CONFLICT

    data = response.json()

    assert data == {'error': 'Category already exists.'}

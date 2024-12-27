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

def test_send_unexpected_param_to_create_category_and_return_error(client):
    payload = {"name": "Drinks", "description": "Beverages category", "unexpected_param": "123"}
    response = client.post("/api/v1/categories", json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_category_name_great_than_limit_and_return_error(client):
    payload = {"name": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "description": "Beverages category"}
    response = client.post("/api/v1/categories", json=payload)

    assert response.status_code == status.HTTP_422

def test_get_category_by_name_and_return_success(client):
    client.post("/api/v1/categories", json={"name": "Drinks", "description": "Beverages category"})
    client.post("/api/v1/categories", json={"name": "Burgers", "description": "Fast food category"})
    
    response = client.get("/api/v1/categories/Burgers/name")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == {
        "id": 2,
        "name": "Burgers",
        "description": "Fast food category"
    }

def test_get_category_by_id_and_return_success(client):
    client.post("/api/v1/categories", json={"name": "Drinks", "description": "Beverages category"})
    client.post("/api/v1/categories", json={"name": "Burgers", "description": "Fast food category"})
    
    response = client.get("/api/v1/categories/1/id")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == {
        "id": 1,
        "name": "Drinks",
        "description": "Beverages category"
    }

def test_get_all_categories_return_success(client):
    client.post("/api/v1/categories", json={"name": "Drinks", "description": "Beverages category"})
    client.post("/api/v1/categories", json={"name": "Burgers", "description": "Fast food category"})
    
    response = client.get("/api/v1/categories")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == [
        {
            "id": 1,
            "name": "Drinks",
            "description": "Beverages category"
        },
        {
            "id": 2,
            "name": "Burgers",
            "description": "Fast food category"
        }
    ]


from fastapi import status

import pytest

from tests.factories.category_factory import CategoryFactory
from tests.factories.product_factory import ProductFactory


@pytest.mark.parametrize("payload", [
    {"name": "Coca-Cola", "description": "Soft drink", "price": 6.99, "category_id": None},
    {"name": "Big Mac", "description": "Fast food burger", "price": 20.99, "category_id": None},
])
def test_create_product_success(client, db_session, payload):
    category = CategoryFactory()
    payload["category_id"] = category.id

    response = client.post("/api/v1/products", json=payload)

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert "id" in data
    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]
    assert data["price"] == payload["price"]
    assert data["category"]["id"] == category.id
    assert data["category"]["name"] == category.name


def test_create_product_duplicate_name_and_return_error(client, db_session):
    category = CategoryFactory()
    ProductFactory(name="Coca-Cola", category=category)

    payload = {
        "name": "Coca-Cola",
        "description": "Soft drink",
        "price": 6.99,
        "category_id": category.id,
    }

    response = client.post("/api/v1/products", json=payload)

    assert response.status_code == status.HTTP_409_CONFLICT

    data = response.json()

    assert data == {"error": "Product already exists."}


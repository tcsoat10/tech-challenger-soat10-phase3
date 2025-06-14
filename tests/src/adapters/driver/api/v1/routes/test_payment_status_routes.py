
from datetime import datetime
from fastapi import status
import pytest

from src.core.exceptions.utils import ErrorCode
from tests.factories.payment_status_factory import PaymentStatusFactory
from src.constants.permissions import PaymentStatusPermissions


@pytest.mark.parametrize("payload", [
  {"name": "Pending", "description": "Payment pending"},
    {"name": "Paid", "description": "Payment paid"},
    {"name": "Canceled", "description": "Payment canceled"},
    {"name": "Refunded", "description": "Payment refunded"},
])
def test_create_payment_status_and_return_success(client, payload):
    response = client.post("/api/v1/payment-status", json=payload, permissions=[PaymentStatusPermissions.CAN_CREATE_PAYMENT_STATUS])

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data == {"id": 1, **payload}

def test_create_payment_status_duplicated_and_return_error(client):
    PaymentStatusFactory(name="Pending", description="Payment pending")

    response = client.post(
        "/api/v1/payment-status",
        json={"name": "Pending", "description": "Payment pending"},
        permissions=[PaymentStatusPermissions.CAN_CREATE_PAYMENT_STATUS]
    )

    assert response.status_code == status.HTTP_409_CONFLICT

    data = response.json()
    assert data == {
        'detail': {
            'code': str(ErrorCode.DUPLICATED_ENTITY),
            'message': 'PaymentStatus already exists.',
            'details': None,
        }
    }

def test_reactivate_payment_status_and_return_success(client):
    PaymentStatusFactory(name="Pending", description="Payment pending", inactivated_at=datetime.now())

    response = client.post("/api/v1/payment-status", json={"name": "Pending", "description": "Payment pending"}, permissions=[PaymentStatusPermissions.CAN_CREATE_PAYMENT_STATUS])

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data == {
        "id": 1,
        "name": "Pending",
        "description": "Payment pending"
    }

def test_send_unexpected_param_to_create_payment_status_and_return_error(client):
    response = client.post(
        "/api/v1/payment-status",
        json={"name": "Pending", "description": "Payment pending", "unexpected_param": "123"},
        permissions=[PaymentStatusPermissions.CAN_CREATE_PAYMENT_STATUS]
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    data = response.json()
    assert data == {
        'detail': [{
            'input': '123',
            'loc': [ 'body', 'unexpected_param' ],
            'msg': 'Extra inputs are not permitted',
            'type': 'extra_forbidden',
        }],
    }

def test_get_payment_status_by_name_and_return_success(client):
    PaymentStatusFactory(name="Pending", description="Payment pending")
    PaymentStatusFactory(name="Paid", description="Payment paid")
    
    response = client.get(
        "/api/v1/payment-status/Paid/name",
        permissions=[PaymentStatusPermissions.CAN_VIEW_PAYMENT_STATUSES]
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == {
        "id": 2,
        "name": "Paid",
        "description": "Payment paid"
    }

def test_get_payment_status_by_id_and_return_success(client):
    PaymentStatusFactory(name="Pending", description="Payment pending")
    PaymentStatusFactory(name="Paid", description="Payment paid")
    
    response = client.get(
        "/api/v1/payment-status/1/id",
        permissions=[PaymentStatusPermissions.CAN_VIEW_PAYMENT_STATUSES]
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == {
        "id": 1,
        "name": "Pending",
        "description": "Payment pending"
   }
    
def test_get_all_payment_status_and_return_success(client):
    PaymentStatusFactory(name="Pending", description="Payment pending")
    PaymentStatusFactory(name="Paid", description="Payment paid")
    
    response = client.get("/api/v1/payment-status", permissions=[PaymentStatusPermissions.CAN_VIEW_PAYMENT_STATUSES])

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == [
        {
            "id": 1,
            "name": "Pending",
            "description": "Payment pending"
        },
        {
            "id": 2,
            "name": "Paid",
            "description": "Payment paid"
        }
    ]

def test_update_payment_status_and_return_success(client):
    PaymentStatusFactory(name="Pending", description="Payment pending")
    PaymentStatusFactory(name="Paid", description="Payment paid")
    
    payload = {
        "id": 1,
        "name": "Pending",
        "description": "Payment pending updated"
    }
    
    response = client.put(
        "/api/v1/payment-status/1",
        json=payload,
        permissions=[PaymentStatusPermissions.CAN_UPDATE_PAYMENT_STATUS]
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == {
        "id": 1,
        "name": "Pending",
        "description": "Payment pending updated"
    }

def test_update_payment_status_not_found_and_return_error(client):
    PaymentStatusFactory(name="Pending", description="Payment pending")
    PaymentStatusFactory(name="Paid", description="Payment paid")
    
    payload = {
        "id": 3,
        "name": "Pending",
        "description": "Payment pending updated"
    }
    
    response = client.put(
        "/api/v1/payment-status/3", json=payload, permissions=[PaymentStatusPermissions.CAN_UPDATE_PAYMENT_STATUS]
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data == {
        'detail': {
            'code': str(ErrorCode.ENTITY_NOT_FOUND),
            'message': 'PaymentStatus not found.',
            'details': None,
        }
    }

def test_delete_payment_status_and_return_success(client):
    PaymentStatusFactory(name="Pending", description="Payment pending")
    PaymentStatusFactory(name="Paid", description="Payment paid")
    
    response = client.delete(
        "/api/v1/payment-status/1", permissions=[PaymentStatusPermissions.CAN_DELETE_PAYMENT_STATUS]
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_delete_payment_status_not_found_and_return_error(client):
    PaymentStatusFactory(name="Pending", description="Payment pending")
    PaymentStatusFactory(name="Paid", description="Payment paid")
    
    response = client.delete(
        "/api/v1/payment-status/3", permissions=[PaymentStatusPermissions.CAN_DELETE_PAYMENT_STATUS]
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()
    assert data == {
        'detail': {
            'code': str(ErrorCode.ENTITY_NOT_FOUND),
            'message': 'PaymentStatus not found.',
            'details': None,
        }
    }

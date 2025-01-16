from tests.factories.person_factory import PersonFactory
from tests.factories.customer_factory import CustomerFactory
from src.core.exceptions.utils import ErrorCode
from src.constants.permissions import CustomerPermissions

from fastapi import status
from datetime import datetime

def test_create_customer_success(client):
    person = PersonFactory()
    payload = {'person_id': person.id}

    response = client.post('/api/v1/customers', json=payload, permissions=[CustomerPermissions.CAN_CREATE_CUSTOMER])
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert 'id' in data
    assert data['person']['id'] == person.id


def test_create_duplicate_customer_return_error(client):
    customer = CustomerFactory()
    payload = {'person_id': customer.person_id}

    response = client.post('/api/v1/customers', json=payload, permissions=[CustomerPermissions.CAN_CREATE_CUSTOMER])
    assert response.status_code == status.HTTP_409_CONFLICT

    data = response.json()

    assert data == {
        'detail': {
            'code': str(ErrorCode.DUPLICATED_ENTITY),
            'message': 'Customer already exists.',
            'details': None,
        }
    }


def test_reactivate_customer_return_success(client):
    customer = CustomerFactory(inactivated_at=datetime.now())
    payload = {'person_id': customer.person_id}

    response = client.post('/api/v1/customers', json=payload, permissions=[CustomerPermissions.CAN_CREATE_CUSTOMER])
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert 'id' in data
    assert data['person']['id'] == customer.person_id


def test_get_customer_by_id_success(client):
    customer = CustomerFactory()

    response = client.get(f'/api/v1/customers/{customer.id}/id', permissions=[CustomerPermissions.CAN_VIEW_CUSTOMERS])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert 'id' in data
    assert data['id'] == customer.id
    assert data['person']['id'] == customer.person_id

def test_get_customer_by_person_id_success(client):
    customer = CustomerFactory()

    response = client.get(f'/api/v1/customers/{customer.person_id}/person_id', permissions=[CustomerPermissions.CAN_VIEW_CUSTOMERS])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert 'id' in data
    assert data['id'] == customer.id
    assert data['person']['id'] == customer.person_id


def test_get_all_customers_success(client):
    customer1 = CustomerFactory()
    customer2 = CustomerFactory()

    response = client.get('/api/v1/customers', permissions=[CustomerPermissions.CAN_VIEW_CUSTOMERS])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == [
        {
            'id': customer1.id,
            'person': {
                'id': customer1.person.id,
                'name': customer1.person.name,
                'cpf': customer1.person.cpf,
                'email': customer1.person.email,
                'birth_date': customer1.person.birth_date.strftime('%Y-%m-%d')
            }
            
        },
        {
            'id': customer2.id,
            'person': {
                'id': customer2.person.id,
                'name': customer2.person.name,
                'cpf': customer2.person.cpf,
                'email': customer2.person.email,
                'birth_date': customer2.person.birth_date.strftime('%Y-%m-%d')
            }
            
        }
    ]


def test_update_customer_success(client):
    person = PersonFactory()
    customer = CustomerFactory()

    payload = {
        'id': customer.id,
        'person_id': person.id
    }

    response = client.put(f'/api/v1/customers/{customer.id}', json=payload, permissions=[CustomerPermissions.CAN_UPDATE_CUSTOMER])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == {
        'id': customer.id,
            'person': {
                'id': person.id,
                'name': person.name,
                'cpf': person.cpf,
                'email': person.email,
                'birth_date': person.birth_date.strftime('%Y-%m-%d')
            }
    }


def test_delete_customer_success(client):
    customer1 = CustomerFactory()
    customer2 = CustomerFactory()

    response = client.delete(f'/api/v1/customers/{customer1.id}', permissions=[CustomerPermissions.CAN_DELETE_CUSTOMER])
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get('/api/v1/customers', permissions=[CustomerPermissions.CAN_VIEW_CUSTOMERS])
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == [{
        'id': customer2.id,
            'person': {
                'id': customer2.person.id,
                'name': customer2.person.name,
                'cpf': customer2.person.cpf,
                'email': customer2.person.email,
                'birth_date': customer2.person.birth_date.strftime('%Y-%m-%d')
            }
    }]
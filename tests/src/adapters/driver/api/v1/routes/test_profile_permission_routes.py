from tests.factories.profile_permission_factory import ProfilePermissionFactory
from tests.factories.permission_factory import PermissionFactory
from tests.factories.profile_factory import ProfileFactory
from src.adapters.driven.repositories.profile_permission_repository import ProfilePermissionRepository

from fastapi import status


def test_create_profile_permission(client, db_session):
    permission = PermissionFactory()
    profile = ProfileFactory()
    payload = {'permission_id': permission.id, 'profile_id': profile.id}
    
    response = client.post('api/v1/profile_permissions', json=payload)

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert 'id' in data
    assert data['permission']['id'] == permission.id
    assert data['profile']['id'] == profile.id


def test_create_duplicate_profile_permission_and_return_error(client, db_session):
    profile_permission = ProfilePermissionFactory()
    payload = {'permission_id': profile_permission.permission_id, 'profile_id': profile_permission.profile_id}
    
    response = client.post('api/v1/profile_permissions', json=payload)

    assert response.status_code == status.HTTP_409_CONFLICT

    data = response.json()

    assert data == {'error': 'Profile Permission already exists.'}


def test_get_profile_permission_by_id_and_return_sucess(client):
    profile_permission_1 = ProfilePermissionFactory()
    profile_permission_2 = ProfilePermissionFactory()

    response = client.get(f'/api/v1/profile_permissions/{profile_permission_2.id}/id')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert 'id' in data
    assert data['id'] == profile_permission_2.id
    assert data['permission']['id'] == profile_permission_2.permission_id
    assert data['profile']['id'] == profile_permission_2.profile_id


def test_get_profile_permission_by_permission_id_and_return_success(client):
    profile_permission_1 = ProfilePermissionFactory()
    profile_permission_2 = ProfilePermissionFactory()

    response = client.get(f'/api/v1/profile_permissions/{profile_permission_2.permission_id}/permission_id')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert 'id' in data
    assert data['permission']['id'] == profile_permission_2.permission_id
    assert data['profile']['id'] == profile_permission_2.profile_id

def test_get_profile_permission_by_profile_id_and_return_success(client):
    profile_permission_1 = ProfilePermissionFactory()
    profile_permission_2 = ProfilePermissionFactory()

    response = client.get(f'/api/v1/profile_permissions/{profile_permission_2.profile_id}/profile_id')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert 'id' in data
    assert data['permission']['id'] == profile_permission_2.permission_id
    assert data['profile']['id'] == profile_permission_2.profile_id


def test_get_all_profile_permissions_return_success(client):
    profile_permission_1 = ProfilePermissionFactory()
    profile_permission_2 = ProfilePermissionFactory()

    response = client.get('/api/v1/profile_permissions')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data == [
        {
            'id': profile_permission_1.id,
            'permission': {
                'id': profile_permission_1.permission.id,
                'name': profile_permission_1.permission.name,
                'description': profile_permission_1.permission.description
            },
            'profile': {
                'id': profile_permission_1.profile.id,
                'name': profile_permission_1.profile.name,
                'description': profile_permission_1.profile.description
            }
        },
        {
            'id': profile_permission_2.id,
            'permission': {
                'id': profile_permission_2.permission.id,
                'name': profile_permission_2.permission.name,
                'description': profile_permission_2.permission.description
            },
            'profile': {
                'id': profile_permission_2.profile.id,
                'name': profile_permission_2.profile.name,
                'description': profile_permission_2.profile.description
            }
        }
    ]
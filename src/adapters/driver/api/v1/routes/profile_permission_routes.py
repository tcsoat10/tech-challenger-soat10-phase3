from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional

from config.database import get_db
from src.core.ports.profile_permission.i_profile_permission_service import IProfilePermissionService
from src.core.ports.profile_permission.i_profile_permission_repository import IProfilePermissionRepository
from src.adapters.driven.repositories.profile_permission_repository import ProfilePermissionRepository
from src.core.ports.permission.i_permission_repository import IPermissionRepository
from src.adapters.driven.repositories.permission_repository import PermissionRepository
from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.adapters.driven.repositories.profile_repository import ProfileRepository
from src.application.services.profile_permission_service import ProfilePermissionService
from src.core.domain.dtos.profile_permission.profile_permission_dto import ProfilePermissionDTO
from src.core.domain.dtos.profile_permission.create_profile_permission_dto import CreateProfilePermissionDTO
from src.core.domain.dtos.profile_permission.update_profile_permission_dto import UpdateProfilePermissionDTO


router = APIRouter()


def _get_profile_permission_service(db_session: Session = Depends(get_db)) -> IProfilePermissionService:
    profile_permission_repository: IProfilePermissionRepository = ProfilePermissionRepository(db_session)
    permission_repository: IPermissionRepository = PermissionRepository(db_session)
    profile_repository: IProfileRepository = ProfileRepository(db_session)
    return ProfilePermissionService(profile_permission_repository, permission_repository, profile_repository)


@router.post('/profile_permissions', response_model=ProfilePermissionDTO, status_code=status.HTTP_201_CREATED)
def create_profile_permission(dto: CreateProfilePermissionDTO, service: IProfilePermissionService = Depends(_get_profile_permission_service)):
    return service.create_profile_permission(dto)


@router.get('/profile_permissions/{profile_permission_id}/id', response_model=ProfilePermissionDTO, status_code=status.HTTP_200_OK)
def get_profile_permission_by_id(profile_permission_id: int, service: IProfilePermissionService = Depends(_get_profile_permission_service)):
    return service.get_profile_permission_by_id(profile_permission_id)


@router.get('/profile_permissions/{permission_id}/permission_id', response_model=ProfilePermissionDTO, status_code=status.HTTP_200_OK)
def get_profile_permission_by_permission_id(permission_id: int, service: IProfilePermissionService = Depends(_get_profile_permission_service)):
    return service.get_profile_permission_by_permission_id(permission_id)


@router.get('/profile_permissions/{profile_id}/profile_id', response_model=ProfilePermissionDTO, status_code=status.HTTP_200_OK)
def get_profile_permission_by_profile_id(profile_id: int, service: IProfilePermissionService = Depends(_get_profile_permission_service)):
    return service.get_profile_permission_by_profile_id(profile_id)


@router.get('/profile_permissions', response_model=List[ProfilePermissionDTO])
def get_all_profile_permissions(include_deleted: Optional[bool] = False, service: IProfilePermissionService = Depends(_get_profile_permission_service)):
    return service.get_all_profile_permissions(include_deleted=include_deleted)


@router.put('/profile_permissions/{profile_permission_id}', response_model=ProfilePermissionDTO)
def update_profile_permission(profile_permission_id: int, dto: UpdateProfilePermissionDTO, service: IProfilePermissionService = Depends(_get_profile_permission_service)):
    return service.update_profile_permission(profile_permission_id, dto)


@router.delete('/profile_permissions/{profile_permission_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_profile_permission(profile_permission_id: int, service: IProfilePermissionService = Depends(_get_profile_permission_service)):
    service.delete_profile_permission(profile_permission_id)

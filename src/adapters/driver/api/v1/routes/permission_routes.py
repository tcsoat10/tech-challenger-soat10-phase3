from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from config.database import get_db
from src.core.ports.permission.i_permission_service import IPermissionService
from src.core.ports.permission.i_permission_repository import IPermissionRepository
from src.adapters.driven.repositories.permission_repository import PermissionRepository
from src.application.services.permission_service import PermissionService
from src.core.domain.dtos.permission.permission_dto import PermissionDTO
from src.core.domain.dtos.permission.create_permission_dto import CreatePermissionDTO
from src.core.domain.dtos.permission.update_permission_dto import UpdatePermissionDTO


router = APIRouter()


def _get_permission_service(db_session: Session = Depends(get_db)) -> IPermissionService:
    repository: IPermissionRepository = PermissionRepository(db_session)
    return PermissionService(repository)


@router.post(path='/permissions', response_model=PermissionDTO, status_code=status.HTTP_201_CREATED)
def create_permission(dto: CreatePermissionDTO, service: IPermissionService = Depends(_get_permission_service)):
    return service.create_permission(dto)


@router.get(path='/permissions/{permission_name}/name', response_model=PermissionDTO, status_code=status.HTTP_200_OK)
def get_permission_by_name(permission_name: str, service: IPermissionService = Depends(_get_permission_service)):
    return service.get_permission_by_name(name=permission_name)


@router.get(path='/permissions/{permission_id}/id', response_model=PermissionDTO, status_code=status.HTTP_200_OK)
def get_permission_by_id(permission_id: int, service: IPermissionService = Depends(_get_permission_service)):
    return service.get_permission_by_id(permission_id)


@router.get(path='/permissions', response_model=List[PermissionDTO], status_code=status.HTTP_200_OK)
def get_all_permissions(service: IPermissionService = Depends(_get_permission_service)):
    return service.get_all_permissions()


@router.put(path='/permission/{permission_id}', response_model=PermissionDTO, status_code=status.HTTP_200_OK)
def update_permission(permission_id: int, dto: UpdatePermissionDTO, service: IPermissionService = Depends(_get_permission_service)):
    return service.update_permission(permission_id, dto)


@router.delete(path='/permissions/{permission_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(permission_id: int, service: IPermissionService = Depends(_get_permission_service)):
    service.delete_permission(permission_id)


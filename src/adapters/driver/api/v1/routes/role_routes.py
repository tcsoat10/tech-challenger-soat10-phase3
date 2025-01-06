from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from config.database import get_db
from src.core.ports.role.i_role_service import IRoleService
from src.core.ports.role.i_role_repository import IRoleRepository
from src.adapters.driven.repositories.role_repository import RoleRepository
from src.application.services.role_service import RoleService
from src.core.domain.dtos.role.create_role_dto import CreateRoleDTO
from src.core.domain.dtos.role.role_dto import RoleDTO
from src.core.domain.dtos.role.update_role_dto import UpdateRoleDTO


router = APIRouter()


def _get_role_service(db_session: Session = Depends(get_db)) -> IRoleService:
    repository: IRoleRepository = RoleRepository(db_session)
    return RoleService(repository)


@router.post('/roles', response_model=RoleDTO, status_code=status.HTTP_201_CREATED)
def create_role(dto: CreateRoleDTO, service: IRoleService = Depends(_get_role_service)):
    return service.create_role(dto)


@router.get('/roles/{role_name}/name', response_model=RoleDTO, status_code=status.HTTP_200_OK)
def get_role_by_name(role_name: str, service: IRoleService = Depends(_get_role_service)):
    return service.get_role_by_name(role_name)


@router.get('/roles/{role_id}/id', response_model=RoleDTO, status_code=status.HTTP_200_OK)
def get_role_by_id(role_id: str, service: IRoleService = Depends(_get_role_service)):
    return service.get_role_by_id(role_id)


@router.get('/roles', response_model=List[RoleDTO], status_code=status.HTTP_200_OK)
def get_all_roles(service: IRoleService = Depends(_get_role_service)):
    return service.get_all_roles()


@router.put('/roles/{role_id}', response_model=RoleDTO, status_code=status.HTTP_200_OK)
def update_role(role_id: int, dto: UpdateRoleDTO, service: IRoleService = Depends(_get_role_service)):
    return service.update_role(role_id, dto)


@router.delete('/roles/{role_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: int, service: IRoleService = Depends(_get_role_service)):
    service.delete_role(role_id)

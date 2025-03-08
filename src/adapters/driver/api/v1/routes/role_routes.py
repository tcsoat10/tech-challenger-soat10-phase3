from fastapi import APIRouter, Depends, Security, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from config.database import get_db
from src.core.auth.dependencies import get_current_user
from src.constants.permissions import RolePermissions
from src.core.ports.role.i_role_service import IRoleService
from src.core.ports.role.i_role_repository import IRoleRepository
from src.adapters.driven.repositories.role_repository import RoleRepository
from src.application.services.role_service import RoleService
from src.core.domain.dtos.role.create_role_dto import CreateRoleDTO
from src.core.domain.dtos.role.role_dto import RoleDTO
from src.core.domain.dtos.role.update_role_dto import UpdateRoleDTO
from src.adapters.driver.api.v1.controllers.role_controller import RoleController


router = APIRouter()


def _get_role_service(db_session: Session = Depends(get_db)) -> IRoleService:
    repository: IRoleRepository = RoleRepository(db_session)
    return RoleService(repository)


def _get_role_controller(db_session: Session = Depends(get_db)) -> RoleController:
    return RoleController(db_session)


@router.post(
    '/roles',
    response_model=RoleDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=[RolePermissions.CAN_CREATE_ROLE])]
)
def create_role(
    dto: CreateRoleDTO,
    controller: RoleController = Depends(_get_role_controller),
    user=Depends(get_current_user)
):
    return controller.create_role(dto)


@router.get(
    '/roles/{role_name}/name',
    response_model=RoleDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[RolePermissions.CAN_VIEW_ROLES])]
)
def get_role_by_name(
    role_name: str,
    controller: RoleController = Depends(_get_role_controller),
    user=Depends(get_current_user)
):
    return controller.get_role_by_name(role_name)


@router.get(
    '/roles/{role_id}/id',
    response_model=RoleDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[RolePermissions.CAN_VIEW_ROLES])]
)
def get_role_by_id(
    role_id: str,
    controller: RoleController = Depends(_get_role_controller),
    user=Depends(get_current_user)
):
    return controller.get_role_by_id(role_id)


@router.get(
    '/roles',
    response_model=List[RoleDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[RolePermissions.CAN_VIEW_ROLES])]
)
def get_all_roles(
    include_deleted: Optional[bool] = Query(False),
    controller: RoleController = Depends(_get_role_controller),
    user=Depends(get_current_user)
):
    return controller.get_all_roles(include_deleted)


@router.put(
    '/roles/{role_id}',
    response_model=RoleDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[RolePermissions.CAN_UPDATE_ROLE])]
)
def update_role(
    role_id: int,
    dto: UpdateRoleDTO,
    controller: RoleController = Depends(_get_role_controller),
    user=Depends(get_current_user)
):
    return controller.update_role(role_id, dto)


@router.delete(
    '/roles/{role_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=[RolePermissions.CAN_DELETE_ROLE])]
)
def delete_role(
    role_id: int,
    controller: RoleController = Depends(_get_role_controller),
    user=Depends(get_current_user)
):
    controller.delete_role(role_id)

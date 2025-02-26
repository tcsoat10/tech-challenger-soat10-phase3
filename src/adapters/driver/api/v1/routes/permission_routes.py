from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.orm import Session
from typing import List

from config.database import get_db
from src.constants.permissions import PermissionPermissions
from src.core.auth.dependencies import get_current_user
from src.core.domain.dtos.permission.permission_dto import PermissionDTO
from src.core.domain.dtos.permission.create_permission_dto import CreatePermissionDTO
from src.core.domain.dtos.permission.update_permission_dto import UpdatePermissionDTO
from src.adapters.driver.api.v1.controllers.permission_controller import PermissionController


router = APIRouter()


def _get_permission_controller(db_session: Session = Depends(get_db)) -> PermissionController:
    return PermissionController(db_session)


@router.post(
    path='/permissions',
    response_model=PermissionDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=[PermissionPermissions.CAN_CREATE_PERMISSION])]
)
def create_permission(
    dto: CreatePermissionDTO,
    controller: PermissionController = Depends(_get_permission_controller),
    user=Depends(get_current_user)
):
    return controller.create_permission(dto)


@router.get(
    path='/permissions/{permission_name}/name',
    response_model=PermissionDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[PermissionPermissions.CAN_VIEW_PERMISSIONS])]
)
def get_permission_by_name(
    permission_name: str,
    controller: PermissionController = Depends(_get_permission_controller),
    user=Depends(get_current_user)
):
    return controller.get_permission_by_name(name=permission_name)


@router.get(
    path='/permissions/{permission_id}/id',
    response_model=PermissionDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[PermissionPermissions.CAN_VIEW_PERMISSIONS])]
)
def get_permission_by_id(
    permission_id: int,
    controller: PermissionController = Depends(_get_permission_controller),
    user=Depends(get_current_user)
):
    return controller.get_permission_by_id(permission_id)


@router.get(
    path='/permissions',
    response_model=List[PermissionDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[PermissionPermissions.CAN_VIEW_PERMISSIONS])]
)
def get_all_permissions(
    controller: PermissionController = Depends(_get_permission_controller),
    user=Depends(get_current_user)
):
    return controller.get_all_permissions()


@router.put(
    path='/permissions/{permission_id}',
    response_model=PermissionDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[PermissionPermissions.CAN_UPDATE_PERMISSION])]
)
def update_permission(
    permission_id: int,
    dto: UpdatePermissionDTO,
    controller: PermissionController = Depends(_get_permission_controller),
    user=Depends(get_current_user)
):
    return controller.update_permission(permission_id, dto)


@router.delete(
    path='/permissions/{permission_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=[PermissionPermissions.CAN_DELETE_PERMISSION])]
)
def delete_permission(
    permission_id: int,
    controller: PermissionController = Depends(_get_permission_controller),
    user=Depends(get_current_user)
):
    controller.delete_permission(permission_id)


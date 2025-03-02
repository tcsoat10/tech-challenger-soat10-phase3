from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.orm import Session
from typing import List

from config.database import get_db
from src.constants.permissions import UserPermissions
from src.core.auth.dependencies import get_current_user
from src.core.ports.user.i_user_service import IUserService
from src.core.ports.user.i_user_repository import IUserRepository
from src.adapters.driven.repositories.user_repository import UserRepository
from src.core.domain.dtos.user.user_dto import UserDTO
from src.core.domain.dtos.user.create_user_dto import CreateUserDTO
from src.application.services.user_service import UserService
from src.core.domain.dtos.user.update_user_dto import UpdateUserDTO
from src.adapters.driver.api.v1.controllers.user_controller import UserController


router = APIRouter()


def _get_user_service(db_session: Session = Depends(get_db)) -> IUserService:
    repository: IUserRepository = UserRepository(db_session)
    return UserService(repository)


def _get_user_controller(db_session: Session = Depends(get_db)) -> UserController:
    return UserController(db_session)


@router.post(
    path='/users',
    response_model=UserDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=[UserPermissions.CAN_CREATE_USER])]
)
def create_user(
    dto: CreateUserDTO,
    controller: UserController = Depends(_get_user_controller),
    user: dict = Security(get_current_user)
):
    return controller.create_user(dto)


@router.get(
    path='/users/{user_name}/name',
    response_model=UserDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[UserPermissions.CAN_VIEW_USERS])]
)
def get_user_by_name(
    user_name: str,
    service: IUserService = Depends(_get_user_service),
    user: dict = Security(get_current_user)
):
    return service.get_user_by_name(user_name)


@router.get(
    path='/users/{user_id}/id',
    response_model=UserDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[UserPermissions.CAN_VIEW_USERS])]
)
def get_user_by_id(
    user_id: int,
    service: IUserService = Depends(_get_user_service),
    user: dict = Security(get_current_user)
):
    return service.get_user_by_id(user_id)


@router.get(
    path='/users',
    response_model=List[UserDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[UserPermissions.CAN_VIEW_USERS])]
)
def get_all_users(
    service: IUserService = Depends(_get_user_service),
    user: dict = Security(get_current_user)
):
    return service.get_all_users()


@router.put(
    path='/users/{user_id}',
    response_model=UserDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[UserPermissions.CAN_UPDATE_USER])]
)
def update_user(
    user_id: int,
    dto: UpdateUserDTO,
    service: IUserService = Depends(_get_user_service),
    user: dict = Security(get_current_user)
):
    return service.update_user(user_id, dto)


@router.delete(
    path='/users/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=[UserPermissions.CAN_DELETE_USER])]
)
def delete_user(
    user_id: int,
    service: IUserService = Depends(_get_user_service),
    user: dict = Security(get_current_user)
):
    service.delete_user(user_id)
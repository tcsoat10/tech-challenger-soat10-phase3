from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Security, status
from sqlalchemy.orm import Session
from dependency_injector.wiring import inject, Provide

from src.adapters.driven.repositories.profile_repository import ProfileRepository
from src.adapters.driven.repositories.user_profile_repository import UserProfileRepository
from src.adapters.driven.repositories.user_repository import UserRepository
from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.core.ports.user.i_user_repository import IUserRepository
from src.core.ports.user_profile.i_user_profile_repository import IUserProfileRepository
from src.constants.permissions import UserProfilePermissions
from src.core.auth.dependencies import get_current_user
from config.database import get_db
from src.core.domain.dtos.user_profile.create_user_profile_dto import CreateUserProfileDTO
from src.core.domain.dtos.user_profile.update_user_profile_dto import UpdateUserProfileDTO
from src.core.domain.dtos.user_profile.user_profile_dto import UserProfileDTO
from src.adapters.driver.api.v1.controllers.user_profile_controller import UserProfileController
from src.core.containers import Container


router = APIRouter()


def _get_user_profile_controller(db_session: Session = Depends(get_db)) -> UserProfileController:
    user_profile_gateway: IUserProfileRepository = UserProfileRepository(db_session)
    profile_gateway: IProfileRepository = ProfileRepository(db_session)
    user_gateway: IUserRepository = UserRepository(db_session)
    return UserProfileController(user_profile_gateway, profile_gateway, user_gateway)


@router.post(
    path='/user-profiles',
    response_model=UserProfileDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=[UserProfilePermissions.CAN_CREATE_USER_PROFILE])]
)
@inject
def create_user_profile(
    dto: CreateUserProfileDTO,
    controller: UserProfileController = Depends(Provide[Container.user_profile_controller]),
    user: dict = Depends(get_current_user)
):
    return controller.create_user_profile(dto)

@router.get(
    path='/user-profiles/{id}',
    response_model=UserProfileDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[UserProfilePermissions.CAN_VIEW_USER_PROFILES])]
)
@inject
def get_user_profile_by_id(
    id: int,
    controller: UserProfileController = Depends(Provide[Container.user_profile_controller]),
    user: dict = Depends(get_current_user)
):
    return controller.get_user_profile_by_id(id)

@router.get(
    path='/user-profiles/{user_id}/{profile_id}',
    response_model=UserProfileDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[UserProfilePermissions.CAN_VIEW_USER_PROFILES])]
)
@inject
def get_user_profile_by_user_id_and_profile_id(
    user_id: int,
    profile_id: int,
    controller: UserProfileController = Depends(Provide[Container.user_profile_controller]),
    user: dict = Depends(get_current_user)
):
    return controller.get_user_profile_by_user_id_and_profile_id(user_id, profile_id)

@router.get(
    path='/user-profiles',
    response_model=List[UserProfileDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[UserProfilePermissions.CAN_VIEW_USER_PROFILES])]
)
@inject
def get_all_user_profiles(
    include_deleted: Optional[bool] = Query(False),
    controller: UserProfileController = Depends(Provide[Container.user_profile_controller]),
    user: dict = Depends(get_current_user)
):
    return controller.get_all_user_profiles(include_deleted=include_deleted)

@router.put(
    path='/user-profiles/{user_profile_id}',
    response_model=UserProfileDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[UserProfilePermissions.CAN_UPDATE_USER_PROFILE])]
)
@inject
def update_user_profile(
    user_profile_id: int,
    dto: UpdateUserProfileDTO,
    controller: UserProfileController = Depends(Provide[Container.user_profile_controller]),
    user: dict = Depends(get_current_user)
):
    return controller.update_user_profile(user_profile_id, dto)

@router.delete(
    path='/user-profiles/{user_profile_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=[UserProfilePermissions.CAN_DELETE_USER_PROFILE])]
)
@inject
def delete_user_profile(
    user_profile_id: int,
    controller: UserProfileController = Depends(Provide[Container.user_profile_controller]),
    user: dict = Depends(get_current_user)
):
    controller.delete_user_profile(user_profile_id)

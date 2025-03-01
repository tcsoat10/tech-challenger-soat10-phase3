from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.orm import Session
from typing import List

from config.database import get_db
from src.constants.permissions import ProfilePermissions
from src.core.auth.dependencies import get_current_user
from src.core.ports.profile.i_profile_service import IProfileService
from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.adapters.driven.repositories.profile_repository import ProfileRepository
from src.application.services.profile_service import ProfileService
from src.core.domain.dtos.profile.profile_dto import ProfileDTO
from src.core.domain.dtos.profile.create_profile_dto import CreateProfileDTO
from src.core.domain.dtos.profile.update_profile_dto import UpdateProfileDTO
from src.adapters.driver.api.v1.controllers.profile_controller import ProfileController


router = APIRouter()


def _get_profile_controller(db_session: Session = Depends(get_db)) -> ProfileController:
    return ProfileController(db_session)


def _get_profile_service(db_session: Session = Depends(get_db)) -> IProfileService:
    repository: IProfileRepository = ProfileRepository(db_session)
    return ProfileService(repository)


@router.post(
    path='/profiles',
    response_model=ProfileDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=[ProfilePermissions.CAN_CREATE_PROFILE])]
)
def create_profile(
    dto: CreateProfileDTO,
    controller: ProfileController = Depends(_get_profile_controller),
    user=Depends(get_current_user)
):
    return controller.create_profile(dto)


@router.get(
    path='/profiles/{profile_name}/name',
    response_model=ProfileDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[ProfilePermissions.CAN_VIEW_PROFILES])]
)
def get_profile_by_name(
    profile_name: str,
    controller: ProfileController = Depends(_get_profile_controller),
    user=Depends(get_current_user)
):
    return controller.get_profile_by_name(name=profile_name)


@router.get(
    path='/profiles/{profile_id}/id',
    response_model=ProfileDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[ProfilePermissions.CAN_VIEW_PROFILES])]
)
def get_profile_by_id(
    profile_id: int,
    controller: ProfileController = Depends(_get_profile_controller),
    user=Depends(get_current_user)
):
    return controller.get_profile_by_id(profile_id)


@router.get(
    path='/profiles',
    response_model=List[ProfileDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[ProfilePermissions.CAN_VIEW_PROFILES])]
)
def get_all_profiles(
    service: IProfileService = Depends(_get_profile_service),
    user=Depends(get_current_user)
):
    return service.get_all_profiles()


@router.put(
    path='/profiles/{profile_id}',
    response_model=ProfileDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[ProfilePermissions.CAN_UPDATE_PROFILE])]
)
def update_profile(
    profile_id: int,
    dto: UpdateProfileDTO,
    service: IProfileService = Depends(_get_profile_service),
    user=Depends(get_current_user)
):
    return service.update_profile(profile_id, dto)


@router.delete(
    path='/profiles/{profile_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=[ProfilePermissions.CAN_DELETE_PROFILE])]
)
def delete_profile(
    profile_id: int,
    service: IProfileService = Depends(_get_profile_service),
    user=Depends(get_current_user)
):
    service.delete_profile(profile_id)


from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.adapters.driven.repositories.profile_repository import ProfileRepository
from src.adapters.driven.repositories.user_repository import UserRepository
from config.database import get_db
from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.core.ports.user.i_user_repository import IUserRepository
from src.application.services.user_profile_service import UserProfileService
from src.adapters.driven.repositories.user_profile_repository import UserProfileRepository
from src.core.domain.dtos.user_profile.create_user_profile_dto import CreateUserProfileDTO
from src.core.domain.dtos.user_profile.update_user_profile_dto import UpdateUserProfileDTO
from src.core.domain.dtos.user_profile.user_profile_dto import UserProfileDTO
from src.core.ports.user_profile.i_user_profile_service import IUserProfileService


router = APIRouter()

def _get_user_profile_service(db_session: Session = Depends(get_db)) -> IUserProfileService:
    repository: IUserProfileService = UserProfileRepository(db_session)
    user_repository: IUserRepository = UserRepository(db_session)
    profile_repository: IProfileRepository = ProfileRepository(db_session)
    return UserProfileService(repository, user_repository, profile_repository)

@router.post(path='/user-profiles', response_model=UserProfileDTO, status_code=status.HTTP_201_CREATED)
def create_user_profile(dto: CreateUserProfileDTO, service: IUserProfileService = Depends(_get_user_profile_service)):
    return service.create_user_profile(dto)

@router.get(path='/user-profiles/{id}', response_model=UserProfileDTO, status_code=status.HTTP_200_OK)
def get_user_profile_by_id(id: int, service: IUserProfileService = Depends(_get_user_profile_service)):
    return service.get_user_profile_by_id(id)

@router.get(path='/user-profiles/{user_id}/{profile_id}', response_model=UserProfileDTO, status_code=status.HTTP_200_OK)
def get_user_profile_by_user_id_and_profile_id(user_id: int, profile_id: int, service: IUserProfileService = Depends(_get_user_profile_service)):
    return service.get_user_profile_by_user_id_and_profile_id(user_id, profile_id)

@router.get(path='/user-profiles', response_model=List[UserProfileDTO], status_code=status.HTTP_200_OK)
def get_all_user_profiles(include_deleted: Optional[bool] = Query(False), service: IUserProfileService = Depends(_get_user_profile_service)):
    return service.get_all_user_profiles(include_deleted=include_deleted)

@router.put(path='/user-profiles/{user_profile_id}', response_model=UserProfileDTO, status_code=status.HTTP_200_OK)
def update_user_profile(user_profile_id: int, dto: UpdateUserProfileDTO, service: IUserProfileService = Depends(_get_user_profile_service)):
    return service.update_user_profile(user_profile_id, dto)

@router.delete(path='/user-profiles/{user_profile_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user_profile(user_profile_id: int, service: IUserProfileService = Depends(_get_user_profile_service)):
    service.delete_user_profile(user_profile_id)

from typing import List, Optional

from config.database import DELETE_MODE
from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.core.ports.user.i_user_repository import IUserRepository
from src.core.domain.entities.user_profile import UserProfile
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.user_profile.i_user_profile_repository import IUserProfileRepository
from src.core.ports.user_profile.i_user_profile_service import IUserProfileService
from src.core.domain.dtos.user_profile.create_user_profile_dto import CreateUserProfileDTO
from src.core.domain.dtos.user_profile.update_user_profile_dto import UpdateUserProfileDTO
from src.core.domain.dtos.user_profile.user_profile_dto import UserProfileDTO

class UserProfileService(IUserProfileService):

    def __init__(self, repository: IUserProfileRepository, user_repository: IUserRepository, profile_repository: IProfileRepository):
        self.repository = repository
        self.user_repository = user_repository
        self.profile_repository = profile_repository

    def create_user_profile(self, dto: CreateUserProfileDTO) -> UserProfileDTO:
        user = self.user_repository.get_by_id(dto.user_id)
        if not user:
            raise EntityNotFoundException(entity_name="User")

        profile = self.profile_repository.get_by_id(dto.profile_id)
        if not profile:
            raise EntityNotFoundException(entity_name="Profile")

        user_profile = self.repository.get_by_user_id_and_profile_id(dto.user_id, dto.profile_id)
        if user_profile:
            if not user_profile.is_deleted():
                raise EntityDuplicatedException(entity_name="UserProfile")
            
            user_profile.reactivate()
            self.repository.update(user_profile)
        else:
            user_profile = UserProfile(user_id=dto.user_id, profile_id=dto.profile_id)
            self.repository.create(user_profile)

        return UserProfileDTO.from_entity(user_profile)
    
    def get_user_profile_by_id(self, id: int) -> UserProfileDTO:
        user_profile = self.repository.get_by_id(id)
        if not user_profile:
            raise EntityNotFoundException(entity_name="UserProfile")
        return UserProfileDTO.from_entity(user_profile)

    def get_user_profile_by_user_id_and_profile_id(self, user_id: int, profile_id: int) -> UserProfileDTO:
        user_profile = self.repository.get_by_user_id_and_profile_id(user_id, profile_id)
        if not user_profile:
            raise EntityNotFoundException(entity_name="UserProfile")
        return UserProfileDTO.from_entity(user_profile)
    
    def get_all_user_profiles(self, include_deleted: Optional[bool] = False) -> List[UserProfileDTO]:
        user_profiles = self.repository.get_all(include_deleted)
        return [UserProfileDTO.from_entity(user_profile) for user_profile in user_profiles]
    
    def update_user_profile(self, user_profile_id: int, dto: UpdateUserProfileDTO) -> UserProfileDTO:
        user = self.user_repository.get_by_id(dto.user_id)
        if not user:
            raise EntityNotFoundException(entity_name="User")

        profile = self.profile_repository.get_by_id(dto.profile_id)
        if not profile:
            raise EntityNotFoundException(entity_name="Profile")

        user_profile = self.repository.get_by_id(user_profile_id)
        if not user_profile:
            raise EntityNotFoundException(entity_name="UserProfile")
        
        user_profile.user_id = dto.user_id
        user_profile.profile_id = dto.profile_id
        self.repository.update(user_profile)
        return UserProfileDTO.from_entity(user_profile)
    
    def delete_user_profile(self, user_profile_id: int) -> None:
        user_profile = self.repository.get_by_id(user_profile_id)
        if not user_profile:
            raise EntityNotFoundException(entity_name="UserProfile")

        if DELETE_MODE == "soft":
            if user_profile.is_deleted():
                raise EntityNotFoundException(entity_name="UserProfile")
            
            user_profile.soft_delete()
            self.repository.update(user_profile)
        else:
            self.repository.delete(user_profile)

__all__ = ["UserProfileService"]

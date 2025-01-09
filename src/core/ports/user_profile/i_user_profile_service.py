from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.domain.dtos.user_profile.create_user_profile_dto import CreateUserProfileDTO
from src.core.domain.dtos.user_profile.update_user_profile_dto import UpdateUserProfileDTO
from src.core.domain.dtos.user_profile.user_profile_dto import UserProfileDTO

class IUserProfileService(ABC):

    @abstractmethod
    def create_user_profile(self, dto: CreateUserProfileDTO) -> UserProfileDTO:
        pass

    @abstractmethod
    def get_user_profile_by_id(self, id: int) -> UserProfileDTO:
        pass

    @abstractmethod
    def get_user_profile_by_user_id_and_profile_id(self, user_id: int, profile_id: int) -> UserProfileDTO:
        pass

    @abstractmethod
    def get_all_user_profiles(self, include_deleted: Optional[bool]) -> List[UserProfileDTO]:
        pass

    @abstractmethod
    def update_user_profile(self, user_profile_id: int, dto: UpdateUserProfileDTO) -> UserProfileDTO:
        pass

    @abstractmethod
    def delete_user_profile(self, user_profile_id: int) -> None:
        pass

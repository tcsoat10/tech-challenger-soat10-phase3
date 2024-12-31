from abc import ABC, abstractmethod
from src.core.domain.dtos.profile.profile_dto import ProfileDTO
from src.core.domain.dtos.profile.create_profile_dto import CreateProfileDTO
from src.core.domain.dtos.profile.update_profile_dto import UpdateProfileDTO
from typing import List


class IProfileService(ABC):
    @abstractmethod
    def create_profile(self, dto: CreateProfileDTO) -> ProfileDTO:
        pass

    @abstractmethod
    def get_profile_by_name(self, name: str) -> ProfileDTO:
        pass

    @abstractmethod
    def get_profile_by_id(self, profile_id: int) -> ProfileDTO:
        pass

    @abstractmethod
    def get_all_profiles(self) -> List[ProfileDTO]:
        pass

    @abstractmethod
    def update_profile(self, profile_id: int, dto: UpdateProfileDTO) -> ProfileDTO:
        pass

    @abstractmethod
    def delete_profile(self, profile_id) -> None:
        pass
from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.domain.dtos.profile_permission.create_profile_permission_dto import CreateProfilePermissionDTO
from src.core.domain.dtos.profile_permission.profile_permission_dto import ProfilePermissionDTO


class IProfilePermissionService(ABC):
    @abstractmethod
    def create_profile_permission(self, dto: CreateProfilePermissionDTO) -> ProfilePermissionDTO:
        pass

    def get_profile_permission_by_id(self, profile_permission_id: int) -> ProfilePermissionDTO:
        pass

    def get_profile_permission_by_permission_id(self, permission_id: int) -> ProfilePermissionDTO:
        pass

    def get_profile_permission_by_permission_id(self, profile_id: int) -> ProfilePermissionDTO:
        pass

    def get_all_profile_permissions(self, include_deleted: Optional[bool] = False) -> List[ProfilePermissionDTO]:
        pass
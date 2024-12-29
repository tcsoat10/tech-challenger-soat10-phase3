from abc import ABC, abstractmethod
from src.core.domain.dtos.permission.permission_dto import PermissionDTO
from src.core.domain.dtos.permission.create_permission_dto import CreatePermissionDTO
from src.core.domain.dtos.permission.update_permission_dto import UpdatePermissionDTO
from typing import List


class IPermissionService(ABC):
    @abstractmethod
    def create_permission(self, dto: CreatePermissionDTO) -> PermissionDTO:
        pass

    @abstractmethod
    def get_permission_by_name(self, name: str) -> PermissionDTO:
        pass

    @abstractmethod
    def get_permission_by_id(self, permission_id: int) -> PermissionDTO:
        pass

    @abstractmethod
    def get_all_permissions(self) -> List[PermissionDTO]:
        pass

    @abstractmethod
    def update_permission(self, permission_id: int, dto: UpdatePermissionDTO) -> PermissionDTO:
        pass

    @abstractmethod
    def delete_permission(self, permission_id) -> None:
        pass
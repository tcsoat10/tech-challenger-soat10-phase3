from abc import ABC, abstractmethod
from typing import List

from src.core.domain.dtos.role.create_role_dto import CreateRoleDTO
from src.core.domain.dtos.role.role_dto import RoleDTO
from src.core.domain.dtos.role.update_role_dto import UpdateRoleDTO


class IRoleService(ABC):
    @abstractmethod
    def create_role(self, dto: CreateRoleDTO) -> RoleDTO:
        pass

    @abstractmethod
    def get_role_by_name(self, name: str) -> RoleDTO:
        pass

    @abstractmethod
    def get_role_by_id(self, role_id: int) -> RoleDTO:
        pass

    @abstractmethod
    def get_all_roles(self) -> List[RoleDTO]:
        pass

    @abstractmethod
    def update_role(self, role_id: int, dto: UpdateRoleDTO) -> RoleDTO:
        pass

    @abstractmethod
    def delete_role(self, role_id: int) -> None:
        pass

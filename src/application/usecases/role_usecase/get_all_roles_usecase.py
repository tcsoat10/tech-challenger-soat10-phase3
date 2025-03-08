from src.core.ports.role.i_role_repository import IRoleRepository
from src.core.domain.entities.role import Role

from typing import List


class GetAllRolesUsecase:
    def __init__(self, role_gateway: IRoleRepository):
        self.role_gateway = role_gateway

    @classmethod
    def build(cls, role_gateway: IRoleRepository) -> 'GetAllRolesUsecase':
        return cls(role_gateway)
    
    def execute(self) -> List[Role]:
        roles = self.role_gateway.get_all()
        return roles
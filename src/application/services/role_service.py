from src.core.ports.role.i_role_service import IRoleService
from src.core.ports.role.i_role_repository import IRoleRepository
from src.core.domain.dtos.role.create_role_dto import CreateRoleDTO
from src.core.domain.dtos.role.role_dto import RoleDTO
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.domain.entities.role import Role
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.domain.dtos.role.update_role_dto import UpdateRoleDTO


class RoleService(IRoleService):
    def __init__(self, repository: IRoleRepository):
        self.repository = repository

    def create_role(self, dto: CreateRoleDTO) -> RoleDTO:
        if self.repository.exists_by_name(dto.name):
            raise EntityDuplicatedException(entity_name='Role')
        
        role = Role(name=dto.name, description=dto.description)
        role = self.repository.create(role)
        return RoleDTO.from_entity(role)

    def get_role_by_name(self, name: str) -> RoleDTO:
        role = self.repository.get_by_name(name)
        if not role:
            raise EntityNotFoundException(entity_name='Role')
        return RoleDTO.from_entity(role)
    
    def get_role_by_id(self, role_id: int) -> RoleDTO:
        role = self.repository.get_by_id(role_id)
        if not role:
            raise EntityNotFoundException(entity_name='Role')
        return RoleDTO.from_entity(role)
    
    def get_all_roles(self):
        roles = self.repository.get_all()
        return [RoleDTO.from_entity(role) for role in roles]
    
    def update_role(self, role_id: int, dto: UpdateRoleDTO) -> RoleDTO:
        role = self.repository.get_by_id(role_id)
        if not role:
            raise EntityNotFoundException(entity_name='Role')
        
        role.name = dto.name
        role.description = dto.description
        updated_role = self.repository.update(role)
        return RoleDTO.from_entity(updated_role)
    
    def delete_role(self, role_id: int) -> None:
        self.repository.delete(role_id)

__all__ = ['RoleService']
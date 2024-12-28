from src.core.ports.permission.i_permission_repository import IPermissionRepository
from src.core.domain.dtos.permission.permission_dto import PermissionDTO
from src.core.domain.dtos.permission.create_permission_dto import CreatePermissionDTO
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.domain.entities.permission import Permission
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException


class PermissionService(IPermissionRepository):
    def __init__(self, repository: IPermissionRepository):
        self.repository = repository

    def create_permission(self, dto: CreatePermissionDTO) -> PermissionDTO:
        if self.repository.exists_by_name(dto.name):
            raise EntityDuplicatedException(entity_name='Permission')
        
        permission = Permission(name=dto.name, description=dto.description)
        permission = self.repository.create(permission)
        return PermissionDTO.from_entity(permission)
    
    def get_permission_by_name(self, name: str) -> PermissionDTO:
        permission = self.repository.get_by_name(name=name)
        if not permission:
            raise EntityNotFoundException(entity_name='Permission')
        return PermissionDTO.from_entity(permission)
    
    def get_permission_by_id(self, permission_id: int) -> PermissionDTO:
        permission = self.repository.get_by_id(permission_id=permission_id)
        if not permission:
            raise EntityNotFoundException(entity_name='Permission')
        return PermissionDTO.from_entity(permission)
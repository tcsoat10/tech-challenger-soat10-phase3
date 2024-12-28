from src.core.ports.permission.i_permission_repository import IPermissionRepository
from src.core.domain.dtos.permission.permission_dto import PermissionDTO
from src.core.domain.dtos.permission.create_permission_dto import CreatePermissionDTO
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.domain.entities.permission import Permission
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from typing import List
from src.core.domain.dtos.permission.update_permission_dto import UpdatePermissionDTO


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
    
    def get_all_permissions(self) -> List[PermissionDTO]:
        permissions = self.repository.get_all()
        return [PermissionDTO.from_entity(permisssion) for permission in permissions]
    
    def update_permission(self, permission_id: int, dto:UpdatePermissionDTO) -> PermissionDTO:
        permission = self.repository.get_by_id(permission_id=permission_id)
        if not permission:
            raise EntityNotFoundException(entity_name='Permission')
        
        permission.name = dto.name
        permission.description = dto.description
        updated_permission = self.repository.update(permission=updated_permission)
        return PermissionDTO.from_entity(updated_permission)
    
    def delete_permission(self, permission_id: int) -> None:
        self.repository.delete(permission_id=permission_id)

__all__ = ['PermissionService']

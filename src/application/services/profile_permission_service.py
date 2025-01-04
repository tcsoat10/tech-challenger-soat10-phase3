from src.core.ports.profile_permission.i_profile_permission_service import IProfilePermissionService
from src.core.ports.profile_permission.i_profile_permission_repository import IProfilePermissionRepository
from src.core.domain.dtos.profile_permission.create_profile_permission_dto import CreateProfilePermissionDTO
from src.core.domain.dtos.profile_permission.profile_permission_dto import ProfilePermissionDTO
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.ports.permission.i_permission_repository import IPermissionRepository
from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.domain.entities.profile_permission import ProfilePermission

from typing import Optional, List


class ProfilePermissionService(IProfilePermissionService):
    def __init__(self, repository: IProfilePermissionRepository, permission_repository: IPermissionRepository, profile_repository: IProfileRepository):
        self.repository = repository
        self.permission_repository = permission_repository
        self.profile_repository = profile_repository

    def create_profile_permission(self, dto: CreateProfilePermissionDTO) -> ProfilePermissionDTO:
        if self.repository.exists_by_permission_id_and_profile_id(dto.permission_id, dto.profile_id):
            raise EntityDuplicatedException(entity_name='Profile Permission')
        
        permission = self.permission_repository.get_by_id(permission_id=dto.permission_id)
        if not permission:
            raise EntityNotFoundException(entity_name='Permission')
        
        profile = self.profile_repository.get_by_id(profile_id=dto.profile_id)
        if not profile:
            raise EntityNotFoundException(entity_name='Profile')
        
        profile_permission = ProfilePermission(permission=permission, profile=profile)
 
        profile_permission = self.repository.create(profile_permission)
        return ProfilePermissionDTO.from_entity(profile_permission)
    
    def get_profile_permission_by_id(self, profile_permission_id: int) -> ProfilePermissionDTO:
        profile_permission = self.repository.get_by_permission_id(profile_permission_id)
        if not profile_permission:
            raise EntityNotFoundException(entity_name='Profile Permission')
        return ProfilePermissionDTO.from_entity(profile_permission)
    
    def get_profile_permission_by_permission_id(self, permission_id: int) -> ProfilePermissionDTO:
        profile_permission = self.repository.get_by_permission_id(permission_id)
        if not profile_permission:
            raise EntityNotFoundException(entity_name='Profile Permission')
        return ProfilePermissionDTO.from_entity(profile_permission)
    
    def get_profile_permission_by_profile_id(self, profile_id: int) -> ProfilePermissionDTO:
        profile_permission = self.repository.get_by_profile_id(profile_id)
        if not profile_permission:
            raise EntityNotFoundException(entity_name='Profile Permission')
        return ProfilePermissionDTO.from_entity(profile_permission)
    
    def get_all_profile_permissions(self, include_deleted: Optional[bool]  = False) -> List[ProfilePermissionDTO]:
        profile_permissions = self.repository.get_all(include_deleted=include_deleted)
        return [ProfilePermissionDTO.from_entity(profile_permission) for profile_permission in profile_permissions]
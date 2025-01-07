from typing import List

from src.core.ports.profile.i_profile_service import IProfileService
from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.core.domain.dtos.profile.profile_dto import ProfileDTO
from src.core.domain.dtos.profile.create_profile_dto import CreateProfileDTO
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.domain.entities.profile import Profile
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.domain.dtos.profile.update_profile_dto import UpdateProfileDTO


class ProfileService(IProfileService):
    def __init__(self, repository: IProfileRepository):
        self.repository = repository

    def create_profile(self, dto: CreateProfileDTO) -> ProfileDTO:
        profile = self.repository.get_by_name(dto.name)
        if profile:
            if not profile.is_deleted():
                raise EntityDuplicatedException(entity_name='Profile')
            
            profile.name = dto.name
            profile.description = dto.description
            profile.reactivate()
            self.repository.update(profile)
        else:
            profile = Profile(name=dto.name, description=dto.description)
            profile = self.repository.create(profile)

        return ProfileDTO.from_entity(profile)
    
    def get_profile_by_name(self, name: str) -> ProfileDTO:
        profile = self.repository.get_by_name(name=name)
        if not profile:
            raise EntityNotFoundException(entity_name='Profile')
        return ProfileDTO.from_entity(profile)
    
    def get_profile_by_id(self, profile_id: int) -> ProfileDTO:
        profile = self.repository.get_by_id(profile_id)
        if not profile:
            raise EntityNotFoundException(entity_name='Profile')
        return ProfileDTO.from_entity(profile)
    
    def get_all_profiles(self) -> List[ProfileDTO]:
        profiles = self.repository.get_all()
        return [ProfileDTO.from_entity(profile) for profile in profiles]
    
    def update_profile(self, profile_id: int, dto:UpdateProfileDTO) -> ProfileDTO:
        profile = self.repository.get_by_id(profile_id)
        if not profile:
            raise EntityNotFoundException(entity_name='Profile')
        
        profile.name = dto.name
        profile.description = dto.description
        updated_profile = self.repository.update(profile)
        return ProfileDTO.from_entity(updated_profile)
    
    def delete_profile(self, profile_id: int) -> None:
        self.repository.delete(profile_id)

__all__ = ['ProfileService']

from src.core.ports.user.i_user_service import IUserService
from src.core.ports.user.i_user_repository import IUserRepository
from src.core.domain.dtos.user.create_user_dto import CreateUserDTO
from src.core.domain.dtos.user.user_dto import UserDTO
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.domain.entities.user import User
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.domain.dtos.user.update_user_dto import UpdateUserDTO

from typing import List


class UserService(IUserService):
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def create_user(self, dto: CreateUserDTO) -> UserDTO:
        user = self.repository.get_by_name(dto.name)
        if user:
            if not user.is_deleted():
                raise EntityDuplicatedException(entity_name='User')
            
            user.name =  dto.name
            user.password = dto.password
            user.reactivate()
            self.repository.update(user)
        else:
            user = User(name=dto.name, password=dto.password)
            user = self.repository.create(user)
        
        return UserDTO.from_entity(user)
    
    def get_user_by_name(self, name: str) -> UserDTO:
        user = self.repository.get_by_name(name)
        if not user:
            raise EntityNotFoundException(entity_name='User')
        return UserDTO.from_entity(user)
    
    def get_user_by_id(self, user_id: int) -> UserDTO:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise EntityNotFoundException(entity_name='User')
        return UserDTO.from_entity(user)
    
    def get_all_users(self) -> List[UserDTO]:
        users = self.repository.get_all()
        return [UserDTO.from_entity(user) for user in users]
    
    def update_user(self, user_id: int, dto: UpdateUserDTO) -> UserDTO:
        user = self.repository.get_by_id(user_id)
        if not user:
            return EntityNotFoundException(entity_name='User')
        
        user.name = dto.name
        user.password = dto.password
        updated_user = self.repository.update(user)
        return UserDTO.from_entity(updated_user)
    
    def delete_user(self, user_id: int) -> None:
        self.repository.delete(user_id)
        
    
__all__ = ['UserService']
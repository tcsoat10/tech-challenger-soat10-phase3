from abc import ABC, abstractmethod
from typing import List

from src.core.domain.dtos.user.create_user_dto import CreateUserDTO
from src.core.domain.dtos.user.user_dto import UserDTO
from src.core.domain.dtos.user.update_user_dto import UpdateUserDTO


class IUserService(ABC):    
    @abstractmethod
    def create_user(self, dto: CreateUserDTO) -> UserDTO:
        pass

    @abstractmethod
    def get_user_by_name(self, name: str) -> UserDTO:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> UserDTO:
        pass

    @abstractmethod
    def get_all_users(self) -> List[UserDTO]:
        pass

    @abstractmethod
    def update_user(self, user_id: int, dto: UpdateUserDTO) -> UserDTO:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        pass
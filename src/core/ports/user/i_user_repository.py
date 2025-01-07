from abc import ABC, abstractmethod

from src.core.domain.entities.user import User


class IUserRepository(ABC):
    @abstractmethod
    def create(user: User):
        pass

    @abstractmethod
    def verify_password(self, password: str, user: User) -> bool:
        pass
    
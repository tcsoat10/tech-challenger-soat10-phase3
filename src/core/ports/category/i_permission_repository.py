from abc import ABC, abstractmethod

from src.core.domain.entities.permission import Permission


class IPermissionRepository(ABC):

    @abstractmethod
    def create(permission: Permission):
        pass

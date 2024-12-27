from abc import ABC, abstractmethod

from src.core.domain.entities.category import Category


class ICategoryRepository(ABC):
    
    @abstractmethod
    def create(category: Category):
        pass

    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        pass

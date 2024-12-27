from abc import ABC, abstractmethod

from src.core.domain.dtos.category.category_dto import CategoryDTO
from src.core.domain.dtos.category.create_category_dto import CreateCategoryDTO


class ICategoryService(ABC):

    @abstractmethod
    def create_category(self, dto: CreateCategoryDTO) -> CategoryDTO:
        pass

    @abstractmethod
    def get_category_by_name(self, name: str) -> CategoryDTO:
        pass

    @abstractmethod
    def get_category_by_id(self, category_id: int) -> CategoryDTO:
        pass

    @abstractmethod
    def get_all_categories(self) -> List[CategoryDTO]:
        pass


from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.domain.dtos.category.update_category_dto import UpdateCategoryDTO
from src.core.domain.dtos.category.category_dto import CategoryDTO
from src.core.domain.dtos.category.create_category_dto import CreateCategoryDTO


class ICategoryService(ABC):

    @abstractmethod
    def update_category(self, category_id: int, dto: UpdateCategoryDTO) -> CategoryDTO:
        pass

    @abstractmethod
    def delete_category(self, category_id: int) -> None:
        pass
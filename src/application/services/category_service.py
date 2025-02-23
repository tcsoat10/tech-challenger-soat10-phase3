from typing import List, Optional
from config.database import DELETE_MODE
from src.core.domain.dtos.category.update_category_dto import UpdateCategoryDTO
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.domain.dtos.category.category_dto import CategoryDTO
from src.core.domain.dtos.category.create_category_dto import CreateCategoryDTO
from src.core.domain.entities.category import Category
from src.core.ports.category.i_category_repository import ICategoryRepository
from src.core.ports.category.i_category_service import ICategoryService


class CategoryService(ICategoryService):

    def __init__(self, repository: ICategoryRepository):
        self.repository = repository

    def delete_category(self, category_id: int) -> None:
        category = self.repository.get_by_id(category_id)
        if not category:
            raise EntityNotFoundException(entity_name="Category")
        
        if DELETE_MODE == 'soft':
            if category.is_deleted():
                raise EntityNotFoundException(entity_name="Category")

            category.soft_delete()
            self.repository.update(category)
        else:
            self.repository.delete(category)

__all__ = ["CategoryService"]

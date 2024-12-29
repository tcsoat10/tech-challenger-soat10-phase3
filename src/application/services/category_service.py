from typing import List
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
    
    def create_category(self, dto: CreateCategoryDTO) -> CategoryDTO:
        if self.repository.exists_by_name(dto.name):
            raise EntityDuplicatedException(entity_name="Category")

        category = Category(name=dto.name, description=dto.description)
        category = self.repository.create(category)
        return CategoryDTO.from_entity(category)
    
    def get_category_by_name(self, name: str) -> CategoryDTO:
        category = self.repository.get_by_name(name=name)
        if not category:
            raise EntityNotFoundException(entity_name="Category")
        return CategoryDTO.from_entity(category)

    def get_category_by_id(self, category_id: int) -> CategoryDTO:
        category = self.repository.get_by_id(category_id=category_id)
        if not category:
            raise EntityNotFoundException(entity_name="Category")
        return CategoryDTO.from_entity(category)

    def get_all_categories(self) -> List[CategoryDTO]:
        categories = self.repository.get_all()
        return [CategoryDTO.from_entity(category) for category in categories]

    def update_category(self, category_id: int, dto: UpdateCategoryDTO) -> CategoryDTO:
        category = self.repository.get_by_id(category_id)
        if not category:
            raise EntityNotFoundException(entity_name="Category")

        category.name = dto.name
        category.description = dto.description
        updated_category = self.repository.update(category)
        return CategoryDTO.from_entity(updated_category)

    def delete_category(self, category_id: int) -> None:
        self.repository.delete(category_id)

__all__ = ["CategoryService"]

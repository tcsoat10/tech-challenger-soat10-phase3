from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.domain.dtos.category.category_dto import CategoryDTO
from src.core.domain.dtos.category.create_category_dto import CreateCategoryDTO
from src.core.domain.entities.category import Category
from src.core.ports.category.i_categorory_repository import ICategoryRepository
from src.core.ports.category.i_category_service import ICategoryService


class CategoryService(ICategoryService):

    def __init__(self, repository: ICategoryRepository):
        self.repository = repository
    
    def create_category(self, dto: CreateCategoryDTO) -> CategoryDTO:
        if self.repository.exists_by_name(dto.name):
            raise EntityDuplicatedException(entity_name="Category")

        category = Category(name=dto.name, description=dto.description)
        category = self.repository.create(category)
        return CategoryDTO(id=category.id, name=category.name, description=category.description)

__all__ = ["CategoryService"]

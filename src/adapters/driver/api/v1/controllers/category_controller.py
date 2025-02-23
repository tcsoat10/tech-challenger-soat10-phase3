
from src.adapters.driven.repositories.category_repository import CategoryRepository
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.health_check_usecase.create_category_usecase import CreateCategoryUseCase
from src.core.domain.dtos.category.category_dto import CategoryDTO
from src.core.domain.dtos.category.create_category_dto import CreateCategoryDTO
from src.core.ports.category.i_category_repository import ICategoryRepository

from sqlalchemy.orm import Session

class CategoryController:
    def __init__(self, db_connection: Session):
        self.category_gateway: ICategoryRepository = CategoryRepository(db_connection)

    def create_category(self, dto: CreateCategoryDTO) -> CategoryDTO:
        create_category_usecase = CreateCategoryUseCase.build(self.category_gateway)
        category = create_category_usecase.execute(dto)
        return DTOPresenter.transform(category, CategoryDTO)

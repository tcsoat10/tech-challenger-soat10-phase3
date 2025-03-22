import pytest
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.domain.dtos.category.update_category_dto import UpdateCategoryDTO
from src.application.usecases.category_usecase.update_category_usecase import UpdateCategoryUseCase
from src.application.usecases.category_usecase.get_category_by_id_usecase import GetCategoryByIdUseCase
from src.application.usecases.category_usecase.get_category_by_name_usecase import GetCategoryByNameUseCase
from src.application.usecases.category_usecase.delete_category_usecase import DeleteCategoryUseCase
from src.application.usecases.category_usecase.get_all_categories_usecase import GetAllCategoriesUseCase
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.adapters.driven.repositories.category_repository import CategoryRepository
from src.application.usecases.category_usecase.create_category_usecase import CreateCategoryUseCase
from src.core.domain.dtos.category.create_category_dto import CreateCategoryDTO

class TestCategoryUseCases:

    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.category_gateway = CategoryRepository(db_session)
        self.create_category_usecase = CreateCategoryUseCase(self.category_gateway)
        self.delete_category_usecase = DeleteCategoryUseCase(self.category_gateway)
        self.get_all_categories_usecase = GetAllCategoriesUseCase(self.category_gateway)
        self.get_by_id_category_usecase = GetCategoryByIdUseCase(self.category_gateway)
        self.get_by_name_category_usecase = GetCategoryByNameUseCase(self.category_gateway)
        self.update_category_usecase = UpdateCategoryUseCase(self.category_gateway)

    def test_create_category_usecase(self):
        dto = CreateCategoryDTO(name='Category 1', description='Description 1')
        category = self.create_category_usecase.execute(dto)

        assert category.id is not None
        assert category.name == 'Category 1'

        category = self.category_gateway.get_by_id(category.id)

        assert category.id is not None
        assert category.name == 'Category 1'

    def test_create_category_usecase_duplicated(self):
        dto = CreateCategoryDTO(name='Category 1', description='Description 1')
        category = self.create_category_usecase.execute(dto)

        assert category.id is not None
        assert category.name == 'Category 1'

        dto = CreateCategoryDTO(name='Category 1', description='Description 1')
        with pytest.raises(EntityDuplicatedException) as exc:
            self.create_category_usecase.execute(dto)
            
        assert str(exc.value) == 'Category already exists.'

    def test_delete_category_usecase_reactivate(self):
        dto = CreateCategoryDTO(name='Category 1', description='Description 1')
        category = self.create_category_usecase.execute(dto)

        self.delete_category_usecase.execute(category.id)
        category = self.category_gateway.get_by_id(category.id)
        
        assert category.is_deleted() is True
        
    def test_list_category_usecase(self):
        dto = CreateCategoryDTO(name='Category 1', description='Description 1')
        self.create_category_usecase.execute(dto)

        dto = CreateCategoryDTO(name='Category 2', description='Description 2')
        self.create_category_usecase.execute(dto)

        categories = self.get_all_categories_usecase.execute()

        assert len(categories) == 2
        assert categories[0].name == 'Category 1'
        assert categories[1].name == 'Category 2'
        
    def test_get_by_id_category_usecase(self):
        dto = CreateCategoryDTO(name='Category 1', description='Description 1')
        category = self.create_category_usecase.execute(dto)

        category = self.get_by_id_category_usecase.execute(category.id)

        assert category is not None
        assert category.id is not None
        assert category.name == 'Category 1'
        assert category.description == 'Description 1'
        assert category.is_deleted() is False

    def test_get_by_name_category_usecase(self):
        dto = CreateCategoryDTO(name='Category 1', description='Description 1')
        self.create_category_usecase.execute(dto)

        category = self.get_by_name_category_usecase.execute('Category 1')

        assert category is not None
        assert category.name == 'Category 1'
        assert category.description == 'Description 1'
        assert category.is_deleted() is False

    def test_update_category_usecase(self):
        dto = CreateCategoryDTO(name='Category 1', description='Description 1')
        category = self.create_category_usecase.execute(dto)

        dto = UpdateCategoryDTO(id=category.id, name='Category 2', description='Description 2')
        self.update_category_usecase.execute(category.id, dto)

        category = self.get_by_name_category_usecase.execute('Category 2')

        assert category is not None
        assert category.name == 'Category 2'
        assert category.description == 'Description 2'
        assert category.is_deleted() is False

    def test_update_category_inexistent_usecase(self):
        dto = UpdateCategoryDTO(id=1, name='Category 2', description='Description 2')
        with pytest.raises(EntityNotFoundException) as exc:
            self.update_category_usecase.execute(1, dto)
            
        assert str(exc.value) == 'Category not found.'

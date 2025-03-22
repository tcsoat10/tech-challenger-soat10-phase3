import pytest
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.domain.dtos.product.create_product_dto import CreateProductDTO
from src.core.domain.dtos.product.update_product_dto import UpdateProductDTO
from src.core.domain.dtos.category.create_category_dto import CreateCategoryDTO
from src.adapters.driven.repositories.product_repository import ProductRepository
from src.adapters.driven.repositories.category_repository import CategoryRepository
from src.application.usecases.product_usecase.create_product_usecase import CreateProductUsecase
from src.application.usecases.product_usecase.get_all_products_usecase import GetAllProductsUseCase
from src.application.usecases.product_usecase.delete_product_usecase import DeleteProductUseCase
from src.application.usecases.product_usecase.update_product_usecase import UpdateProductUsecase
from src.application.usecases.category_usecase.create_category_usecase import CreateCategoryUseCase

class TestProductUsecases:

    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.product_gateway = ProductRepository(db_session)
        self.category_gateway = CategoryRepository(db_session)
        self.create_product_usecase = CreateProductUsecase(self.product_gateway, self.category_gateway)
        self.get_all_products_usecase = GetAllProductsUseCase(self.product_gateway)
        self.delete_product_usecase = DeleteProductUseCase(self.product_gateway)
        self.update_product_usecase = UpdateProductUsecase(self.product_gateway, self.category_gateway)
        self.create_category_usecase = CreateCategoryUseCase(self.category_gateway)

    def test_create_product_usecase(self):
        category_dto = CreateCategoryDTO(name='Test Category', description='Test Description')
        category = self.create_category_usecase.execute(category_dto)

        dto = CreateProductDTO(
            name='Product 1',
            description='Description 1',
            price=10.0,
            category_id=category.id
        )
        
        product = self.create_product_usecase.execute(dto)

        assert product.id is not None
        assert product.name == 'Product 1'
        assert product.category.id == category.id

    def test_create_product_duplicate_usecase(self):
        category_dto = CreateCategoryDTO(name='Test Category', description='Test Description')
        category = self.create_category_usecase.execute(category_dto)

        dto = CreateProductDTO(
            name='Product 1',
            description='Description 1',
            price=10.0,
            category_id=category.id
        )
        
        self.create_product_usecase.execute(dto)

        with pytest.raises(EntityDuplicatedException):
            self.create_product_usecase.execute(dto)

    def test_get_all_products_usecase(self):
        category_dto = CreateCategoryDTO(name='Test Category', description='Test Description')
        category = self.create_category_usecase.execute(category_dto)

        dto1 = CreateProductDTO(
            name='Product 1',
            description='Description 1',
            price=10.0,
            category_id=category.id
        )
        
        dto2 = CreateProductDTO(
            name='Product 2',
            description='Description 2',
            price=20.0,
            category_id=category.id
        )
        
        self.create_product_usecase.execute(dto1)
        self.create_product_usecase.execute(dto2)

        products = self.get_all_products_usecase.execute(categories=None)

        assert len(products) == 2
        assert products[0].name == 'Product 1'
        assert products[1].name == 'Product 2'

    def test_delete_product_usecase(self):
        category_dto = CreateCategoryDTO(name='Test Category', description='Test Description')
        category = self.create_category_usecase.execute(category_dto)

        dto = CreateProductDTO(
            name='Product 1',
            description='Description 1',
            price=10.0,
            category_id=category.id
        )
        
        product = self.create_product_usecase.execute(dto)
        self.delete_product_usecase.execute(product.id)

        assert product.is_deleted() is True

    def test_update_product_usecase(self):
        category_dto = CreateCategoryDTO(name='Test Category', description='Test Description')
        category = self.create_category_usecase.execute(category_dto)

        create_dto = CreateProductDTO(
            name='Product 1',
            description='Description 1',
            price=10.0,
            category_id=category.id
        )
        
        product = self.create_product_usecase.execute(create_dto)

        update_dto = UpdateProductDTO(
            id=product.id,
            name='Product Updated',
            description='Description Updated',
            price=15.0,
            category_id=category.id
        )

        updated_product = self.update_product_usecase.execute(product.id, update_dto)

        assert updated_product.name == 'Product Updated'
        assert updated_product.description == 'Description Updated'
        assert updated_product.price == 15.0

    def test_update_product_not_found_usecase(self):
        update_dto = UpdateProductDTO(
            id=1,
            name='Product Updated',
            description='Description Updated',
            price=15.0,
            category_id=1
        )

        with pytest.raises(EntityNotFoundException):
            self.update_product_usecase.execute(1, update_dto)



from typing import List, Optional
from src.application.usecases.product_usecase.update_product_usecase import UpdateProductUsecase
from src.application.usecases.product_usecase.get_all_products_usecase import GetAllProductsUseCase
from src.application.usecases.product_usecase.get_product_by_id_usecase import GetProductByIdUseCase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.product_usecase.create_product_usecase import CreateProductUsecase
from src.core.domain.dtos.product.create_product_dto import CreateProductDTO
from src.core.domain.dtos.product.product_dto import ProductDTO
from src.adapters.driven.repositories.category_repository import CategoryRepository
from src.adapters.driven.repositories.product_repository import ProductRepository
from src.core.ports.category.i_category_repository import ICategoryRepository
from src.core.ports.product.i_product_repository import IProductRepository
from src.application.usecases.product_usecase.get_product_by_name_usecase import GetProductByNameUseCase

from sqlalchemy.orm import Session

class ProductController:
    def __init__(self, db_connection: Session):
        self.product_gateway: IProductRepository = ProductRepository(db_connection)
        self.category_gateway: ICategoryRepository = CategoryRepository(db_connection)

    def create_product(self, dto: CreateProductDTO) -> ProductDTO:
        create_product_usecase = CreateProductUsecase.build(self.product_gateway, self.category_gateway)
        product = create_product_usecase.execute(dto)
        return DTOPresenter.transform(product, ProductDTO)    
    
    def get_product_by_name(self, name: str) -> ProductDTO:
        product_by_name = GetProductByNameUseCase.build(self.product_gateway)
        product = product_by_name.execute(name)
        return DTOPresenter.transform(product, ProductDTO)
    
    def get_product_by_id(self, product_id: int) -> ProductDTO:
        get_product_by_id_usecase = GetProductByIdUseCase.build(self.product_gateway)
        product = get_product_by_id_usecase.execute(product_id)
        return DTOPresenter.transform(product, ProductDTO)
    
    def get_all_products(self, categories: Optional[List[str]], include_deleted: Optional[bool] = False) -> list[ProductDTO]:
        all_products_usecase = GetAllProductsUseCase.build(self.product_gateway)
        products = all_products_usecase.execute(categories, include_deleted)
        return DTOPresenter.transform_list(products, ProductDTO)

    def update_product(self, product_id: int, dto: CreateProductDTO) -> ProductDTO:
        update_product_usecase = UpdateProductUsecase.build(self.product_gateway, self.category_gateway)
        product = update_product_usecase.execute(product_id, dto)
        return DTOPresenter.transform(product, ProductDTO)

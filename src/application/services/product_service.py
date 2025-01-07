from typing import List, Optional
from config.database import DELETE_MODE
from src.core.domain.dtos.product.update_product_dto import UpdateProductDTO
from src.core.domain.dtos.product.create_product_dto import CreateProductDTO
from src.core.domain.dtos.product.product_dto import ProductDTO
from src.core.ports.category.i_category_repository import ICategoryRepository
from src.core.domain.entities.product import Product
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.product.i_product_repository import IProductRepository
from src.core.ports.product.i_product_service import IProductService


class ProductService(IProductService):

    def __init__(self, repository: IProductRepository, category_repository: ICategoryRepository):
        self.repository = repository
        self.category_repository = category_repository
    
    def create_product(self, dto: CreateProductDTO) -> ProductDTO:
        category = self.category_repository.get_by_id(category_id=dto.category_id)
        if not category:
            raise EntityNotFoundException(entity_name="Category")

        product = self.repository.get_by_name(name=dto.name)
        if product:
            if not product.is_deleted():
                raise EntityDuplicatedException(entity_name="Product")
            
            product.name = dto.name
            product.description = dto.description
            product.price = dto.price
            product.category = category
            product.reactivate()
            self.repository.update(product)
        else:
            product = Product(name=dto.name, description=dto.description, price=dto.price, category=category)
            product = self.repository.create(product)

        return ProductDTO.from_entity(product)
    
    def get_product_by_name(self, name: str) -> ProductDTO:
        product = self.repository.get_by_name(name=name)
        if not product:
            raise EntityNotFoundException(entity_name="Product")
        return ProductDTO.from_entity(product)

    def get_product_by_id(self, product_id: int) -> ProductDTO:
        product = self.repository.get_by_id(product_id=product_id)
        if not product:
            raise EntityNotFoundException(entity_name="Product")
        return ProductDTO.from_entity(product)

    def get_all_products(self, include_deleted: Optional[bool] = False) -> List[ProductDTO]:
        products = self.repository.get_all(include_deleted=include_deleted)
        return [ProductDTO.from_entity(product) for product in products]

    def update_product(self, product_id: int, dto: UpdateProductDTO) -> ProductDTO:
        product = self.repository.get_by_id(product_id)
        if not product:
            raise EntityDuplicatedException(entity_name="Product")
        
        category = self.category_repository.get_by_id(category_id=dto.category_id)
        if not category:
            raise EntityNotFoundException(entity_name="Category")

        product.name=dto.name,
        product.description=dto.description,
        product.price=dto.price,
        product.category=category

        product = self.repository.update(product)

        return ProductDTO.from_entity(product)

    def delete_product(self, product_id: int) -> None:
        product = self.repository.get_by_id(product_id)
        if not product:
            raise EntityNotFoundException(entity_name="Product")
        
        if DELETE_MODE == 'soft':
            if product.is_deleted():
                raise EntityNotFoundException(entity_name="Product")

            product.soft_delete()
            self.repository.update(product)
        else:
            self.repository.delete(product)

__all__ = ["ProductService"]

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
        if self.repository.exists_by_name(dto.name):
            raise EntityDuplicatedException(entity_name="Product")
        
        category = self.category_repository.get_by_id(category_id=dto.category_id)
        if not category:
            raise EntityNotFoundException(entity_name="Category")

        product = Product(
            name=dto.name,
            description=dto.description,
            price=dto.price,
            category=category,
        )

        product = self.repository.create(product)
        return ProductDTO.from_entity(product)
    
    def get_product_by_name(self, name: str) -> ProductDTO:
        product = self.repository.get_by_name(name=name)
        if not product:
            raise EntityNotFoundException(entity_name="Product")
        return ProductDTO.from_entity(product)


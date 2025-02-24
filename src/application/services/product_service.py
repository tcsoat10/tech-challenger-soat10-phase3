
from config.database import DELETE_MODE
from src.core.ports.category.i_category_repository import ICategoryRepository
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.product.i_product_repository import IProductRepository
from src.core.ports.product.i_product_service import IProductService


class ProductService(IProductService):

    def __init__(self, repository: IProductRepository, category_repository: ICategoryRepository):
        self.repository = repository
        self.category_repository = category_repository

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

from abc import ABC, abstractmethod
from typing import List, Optional
from src.core.domain.dtos.product.update_product_dto import UpdateProductDTO
from src.core.domain.dtos.product.product_dto import ProductDTO


class IProductService(ABC):

    @abstractmethod
    def get_product_by_id(self, product_id: int) -> ProductDTO:
        pass

    @abstractmethod
    def get_all_products(self, include_deleted: Optional[bool] = False) -> List[ProductDTO]:
        pass

    @abstractmethod
    def update_product(self, product_id: int, dto: UpdateProductDTO) -> ProductDTO:
        pass

    @abstractmethod
    def delete_product(self, product_id: int) -> None:
        pass

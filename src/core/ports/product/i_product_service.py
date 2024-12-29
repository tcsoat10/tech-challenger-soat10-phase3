from abc import ABC, abstractmethod
from typing import List
from src.core.domain.dtos.product.update_product_dto import UpdateProductDTO
from src.core.domain.dtos.product.product_dto import ProductDTO
from src.core.domain.dtos.product.create_product_dto import CreateProductDTO


class IProductService(ABC):

    @abstractmethod
    def create_product(self, dto: CreateProductDTO) -> ProductDTO:
        pass

    @abstractmethod
    def get_product_by_name(self, name: str) -> ProductDTO:
        pass

    @abstractmethod
    def get_product_by_id(self, product_id: int) -> ProductDTO:
        pass

    @abstractmethod
    def get_all_products(self) -> List[ProductDTO]:
        pass

    @abstractmethod
    def update_product(self, product_id: int, dto: UpdateProductDTO) -> ProductDTO:
        pass

    @abstractmethod
    def delete_product(self, product_id: int) -> None:
        pass

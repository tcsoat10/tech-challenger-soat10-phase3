from abc import ABC, abstractmethod
from src.core.domain.dtos.product.product_dto import ProductDTO
from src.core.domain.dtos.product.create_product_dto import CreateProductDTO


class IProductService(ABC):

    @abstractmethod
    def create_product(self, dto: CreateProductDTO) -> ProductDTO:
        pass


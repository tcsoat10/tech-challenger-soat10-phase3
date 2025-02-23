from abc import ABC, abstractmethod
from src.core.domain.dtos.product.update_product_dto import UpdateProductDTO
from src.core.domain.dtos.product.product_dto import ProductDTO


class IProductService(ABC):

    @abstractmethod
    def update_product(self, product_id: int, dto: UpdateProductDTO) -> ProductDTO:
        pass

    @abstractmethod
    def delete_product(self, product_id: int) -> None:
        pass

from abc import ABC, abstractmethod
from typing import List

from src.core.domain.entities.product import Product


class IProductRepository(ABC):
    
    @abstractmethod
    def create(category: Product):
        pass

    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Product:
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Product:
        pass

    @abstractmethod
    def get_all(self) -> List[Product]:
        pass

    @abstractmethod
    def update(self, product: Product) -> Product:
        pass
    

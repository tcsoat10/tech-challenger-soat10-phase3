from abc import ABC, abstractmethod

from src.core.domain.entities.product import Product


class IProductRepository(ABC):
    
    @abstractmethod
    def create(category: Product):
        pass


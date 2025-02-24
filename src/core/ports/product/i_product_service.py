from abc import ABC, abstractmethod


class IProductService(ABC):

    @abstractmethod
    def delete_product(self, product_id: int) -> None:
        pass

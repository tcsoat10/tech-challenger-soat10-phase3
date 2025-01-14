from abc import ABC, abstractmethod
from typing import List

from src.core.domain.entities.order import Order


class IOrderRepository(ABC):
    
    @abstractmethod
    def create(order: Order):
        pass

    @abstractmethod
    def get_by_customer_id(self, id_customer: int) -> List[Order]:
        pass

    @abstractmethod
    def get_by_employee_id(self, id_employee: int) -> List[Order]:
        pass

    @abstractmethod
    def get_by_id(self, order_id: int) -> Order:
        pass

    @abstractmethod
    def get_all(self, include_deleted: bool = False) -> List[Order]:
        pass

    @abstractmethod
    def update(self, order: Order) -> Order:
        pass

    @abstractmethod
    def delete(self, order: int) -> Order:
        pass

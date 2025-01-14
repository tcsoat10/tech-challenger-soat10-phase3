from abc import ABC, abstractmethod
from typing import List

from src.core.domain.dtos.order.update_order_dto import UpdateOrderDTO
from src.core.domain.dtos.order.order_dto import OrderDTO
from src.core.domain.dtos.order.create_order_dto import CreateOrderDTO


class IOrderService(ABC):

    @abstractmethod
    def create_order(self, dto: CreateOrderDTO) -> OrderDTO:
        pass

    @abstractmethod
    def get_order_by_customer_id(self, id_customer: int) -> List[OrderDTO]:
        pass

    @abstractmethod
    def get_order_by_employee_id(self, id_employee: int) -> List[OrderDTO]:
        pass
    
    @abstractmethod
    def get_order_by_id(self, order_id: int) -> OrderDTO:
        pass

    @abstractmethod
    def get_all_orders(self, include_deleted: bool = False) -> List[OrderDTO]:
        pass

    @abstractmethod
    def update_order(self, order_id: int, dto: UpdateOrderDTO) -> OrderDTO:
        pass

    @abstractmethod
    def delete_order(self, order_id: int, dto: UpdateOrderDTO) -> OrderDTO:
        pass
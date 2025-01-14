from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.domain.dtos.order_status.update_order_status_dto import UpdateOrderStatusDTO
from src.core.domain.dtos.order_status.order_status_dto import OrderStatusDTO
from src.core.domain.dtos.order_status.create_order_status_dto import CreateOrderStatusDTO


class IOrderStatusService(ABC):

    @abstractmethod
    def create_order_status(self, dto: CreateOrderStatusDTO) -> OrderStatusDTO:
        pass

    @abstractmethod
    def get_order_status_by_status(self, status: str) -> OrderStatusDTO:
        pass
    
    @abstractmethod
    def get_order_status_by_id(self, order_id: int) -> OrderStatusDTO:
        pass

    @abstractmethod
    def get_all_orders_status(self, include_deleted: Optional[bool] = False) -> List[OrderStatusDTO]:
        pass

    @abstractmethod
    def update_order_status(self, order_id: int, dto: UpdateOrderStatusDTO) -> OrderStatusDTO:
        pass

    @abstractmethod
    def delete_order_status(self, order_id: int, dto: UpdateOrderStatusDTO) -> OrderStatusDTO:
        pass
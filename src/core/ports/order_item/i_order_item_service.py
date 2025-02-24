from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.domain.dtos.order_item.update_order_item_dto import UpdateOrderItemDTO
from src.core.domain.dtos.order_item.order_item_dto import OrderItemDTO


class IOrderItemService(ABC):

    @abstractmethod
    def update_order_item(self, order_item_id: int, dto: UpdateOrderItemDTO) -> OrderItemDTO:
        pass

    @abstractmethod
    def delete_order_item(self, order_item_id: int) -> None:
        pass

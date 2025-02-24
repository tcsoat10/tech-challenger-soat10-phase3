from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.domain.dtos.order_item.update_order_item_dto import UpdateOrderItemDTO
from src.core.domain.dtos.order_item.create_order_item_dto import CreateOrderItemDTO
from src.core.domain.dtos.order_item.order_item_dto import OrderItemDTO


class IOrderItemService(ABC):

    @abstractmethod
    def get_order_item_by_order_id(self, order_id: int, include_deleted: bool = False) -> List[OrderItemDTO]:
        pass

    @abstractmethod
    def get_order_item_by_product_name(self, order_id: int, product_name: str) -> OrderItemDTO:
        pass

    @abstractmethod
    def get_order_item_by_id(self, order_item_id: int) -> OrderItemDTO:
        pass

    @abstractmethod
    def get_all_order_items(self, include_deleted: Optional[bool] = False) -> List[OrderItemDTO]:
        pass

    @abstractmethod
    def update_order_item(self, order_item_id: int, dto: UpdateOrderItemDTO) -> OrderItemDTO:
        pass

    @abstractmethod
    def delete_order_item(self, order_item_id: int) -> None:
        pass

from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.domain.dtos.order.order_dto import OrderDTO
from src.core.domain.dtos.order.create_order_dto import CreateOrderDTO


class IOrderService(ABC):

    @abstractmethod
    def add_item(self, order_id: int, item_dto: CreateOrderDTO, current_user: dict) -> None:
        pass

    @abstractmethod
    def remove_item(self, order_id: int, item_id: int, current_user: dict) -> None:
        pass

    @abstractmethod
    def change_item_quantity(self, order_id: int, item_id: int, new_quantity: int, current_user: dict) -> None:
        pass

    @abstractmethod
    def change_item_observation(self, order_id: int, item_id: int, new_observation: str, current_user: dict) -> None:
        pass

    @abstractmethod
    def clear_order(self, order_id: int, current_user: dict) -> None:
        pass

    @abstractmethod
    def list_order_items(self, order_id: int, current_user: dict) -> List[OrderDTO]:
        pass

    @abstractmethod
    def cancel_order(self, order_id: int, current_user: dict) -> None:
        pass

    @abstractmethod
    def next_step(self, order_id: int, current_user: dict) -> None:
        pass

    @abstractmethod
    def go_back(self, order_id: int, current_user: dict) -> None:
        pass

    @abstractmethod
    def list_orders(self, current_user: dict, status: Optional[List[str]]) -> List[OrderDTO]:
        pass

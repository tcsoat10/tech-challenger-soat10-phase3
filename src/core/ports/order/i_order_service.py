from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.domain.dtos.order.order_dto import OrderDTO


class IOrderService(ABC):

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

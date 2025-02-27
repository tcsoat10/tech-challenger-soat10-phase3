from abc import ABC, abstractmethod


class IOrderService(ABC):

    @abstractmethod
    def next_step(self, order_id: int, current_user: dict) -> None:
        pass

    @abstractmethod
    def go_back(self, order_id: int, current_user: dict) -> None:
        pass

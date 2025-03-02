from abc import ABC, abstractmethod


class IOrderService(ABC):

    @abstractmethod
    def go_back(self, order_id: int, current_user: dict) -> None:
        pass

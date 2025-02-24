from abc import ABC, abstractmethod


class IOrderItemService(ABC):

    @abstractmethod
    def delete_order_item(self, order_item_id: int) -> None:
        pass

from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.domain.dtos.order_status.update_order_status_dto import UpdateOrderStatusDTO
from src.core.domain.dtos.order_status.order_status_dto import OrderStatusDTO
from src.core.domain.dtos.order_status.create_order_status_dto import CreateOrderStatusDTO


class IOrderStatusService(ABC):

    @abstractmethod
    def delete_order_status(self, order_id: int, dto: UpdateOrderStatusDTO) -> OrderStatusDTO:
        pass
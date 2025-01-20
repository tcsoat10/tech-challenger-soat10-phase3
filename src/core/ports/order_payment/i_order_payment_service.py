from abc import ABC, abstractmethod

from src.core.domain.dtos.order_payment.create_order_payment_dto import CreateOrderPaymentDTO
from src.core.domain.dtos.order_payment.order_payment_dto import OrderPaymentDTO


class IOrderPaymentService(ABC):
    @abstractmethod
    def create_order_payment(self, dto: CreateOrderPaymentDTO) -> OrderPaymentDTO:
        pass
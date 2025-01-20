from abc import ABC, abstractmethod

from src.core.domain.entities.order_payment import OrderPayment


class IOrderPaymentRepository(ABC):
    @abstractmethod
    def create(self, order_payment: OrderPayment) -> OrderPayment:
        pass
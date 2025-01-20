from abc import ABC, abstractmethod
from typing import List

from src.core.domain.entities.order_payment import OrderPayment


class IOrderPaymentRepository(ABC):
    @abstractmethod
    def create(self, order_payment: OrderPayment) -> OrderPayment:
        pass

    @abstractmethod
    def get_by_id(self, order_payment_id: int) -> OrderPayment:
        pass

    @abstractmethod
    def get_by_order_id(self, order_id: int) -> OrderPayment:
        pass

    @abstractmethod
    def get_by_payment_id(self, payment_id: int) -> OrderPayment:
        pass

    @abstractmethod
    def get_all(self) -> List[OrderPayment]:
        pass

    @abstractmethod
    def update(self, order_payment: OrderPayment) -> OrderPayment:
        pass
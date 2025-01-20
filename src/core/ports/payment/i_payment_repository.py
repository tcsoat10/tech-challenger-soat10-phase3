from abc import ABC, abstractmethod
from typing import List

from src.core.domain.entities.payment import Payment


class IPaymentRepository(ABC):
    @abstractmethod
    def create(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    def get_by_id(self, payment_id: int) -> Payment:
        pass

    @abstractmethod
    def get_by_method_id(self, method_id: int) -> List[Payment]:
        pass

    @abstractmethod
    def get_by_status_id(self, status_id: int) -> List[Payment]:
        pass

    @abstractmethod
    def get_all(self) -> List[Payment]:
        pass

    @abstractmethod
    def update(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    def delete(self, payment_id: int) -> None:
        pass
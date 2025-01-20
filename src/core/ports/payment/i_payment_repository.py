from abc import ABC, abstractmethod

from src.core.domain.entities.payment import Payment


class IPaymentRepository(ABC):
    @abstractmethod
    def create(self, payment: Payment) -> Payment:
        pass
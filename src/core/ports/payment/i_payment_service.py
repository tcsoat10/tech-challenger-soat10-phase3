from abc import ABC, abstractmethod

from src.core.domain.dtos.payment.create_payment_dto import CreatePaymentDTO
from src.core.domain.dtos.payment.payment_dto import PaymentDTO


class IPaymentService(ABC):
    @abstractmethod
    def create_payment(self, dto: CreatePaymentDTO) -> PaymentDTO:
        pass

    @abstractmethod
    def get_payment_by_id(self, payment_id: int) -> PaymentDTO:
        pass
from abc import ABC, abstractmethod
from typing import List

from src.core.domain.dtos.payment.create_payment_dto import CreatePaymentDTO
from src.core.domain.dtos.payment.payment_dto import PaymentDTO


class IPaymentService(ABC):
    @abstractmethod
    def create_payment(self, dto: CreatePaymentDTO) -> PaymentDTO:
        pass

    @abstractmethod
    def get_payment_by_id(self, payment_id: int) -> PaymentDTO:
        pass

    @abstractmethod
    def get_payments_by_method_id(self, method_id: int) -> List[PaymentDTO]:
        pass

    
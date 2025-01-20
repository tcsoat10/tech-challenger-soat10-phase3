from abc import ABC, abstractmethod
from typing import List

from src.core.domain.dtos.payment.create_payment_dto import CreatePaymentDTO
from src.core.domain.dtos.payment.payment_dto import PaymentDTO
from src.core.domain.dtos.payment.update_payment_dto import UpdatePaymentDTO


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
    
    @abstractmethod
    def get_payments_by_status_id(self, status_id: int) -> List[PaymentDTO]:
        pass

    @abstractmethod
    def get_all_payments(self, include_deleted: bool = False) -> List[PaymentDTO]:
        pass
    
    @abstractmethod
    def update_payment(self, payment_id: int, dto: UpdatePaymentDTO) -> PaymentDTO:
        pass

    @abstractmethod
    def delete_payment(self, payment_id: int) -> None:
        pass
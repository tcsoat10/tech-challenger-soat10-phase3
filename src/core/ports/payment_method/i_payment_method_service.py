from abc import ABC, abstractmethod
from typing import Optional

from src.core.domain.dtos.payment_method.create_payment_method_dto import CreatePaymentMethodDTO
from src.core.domain.dtos.payment_method.payment_method_dto import PaymentMethodDTO

class IPaymentMethodService(ABC):

    @abstractmethod
    def create_payment_method(self, dto: CreatePaymentMethodDTO) -> PaymentMethodDTO:
        pass

    @abstractmethod
    def get_payment_method_by_name(self, name: str) -> PaymentMethodDTO:
        pass

    @abstractmethod
    def get_payment_method_by_id(self, payment_method_id: int) -> PaymentMethodDTO:
        pass

    @abstractmethod
    def get_all_payment_methods(self, include_deleted: Optional[bool] = False) -> list[PaymentMethodDTO]:
        pass

    @abstractmethod
    def update_payment_method(self, payment_method_id: int, dto: CreatePaymentMethodDTO) -> PaymentMethodDTO:
        pass

    @abstractmethod
    def delete_payment_method(self, payment_method_id: int) -> None:
        pass

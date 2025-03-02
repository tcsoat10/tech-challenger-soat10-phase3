from abc import ABC, abstractmethod
from typing import Optional

from src.core.domain.dtos.payment_method.create_payment_method_dto import CreatePaymentMethodDTO
from src.core.domain.dtos.payment_method.payment_method_dto import PaymentMethodDTO

class IPaymentMethodService(ABC):

    @abstractmethod
    def delete_payment_method(self, payment_method_id: int) -> None:
        pass

from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.domain.dtos.payment_status.update_payment_status_dto import UpdatePaymentStatusDTO
from src.core.domain.dtos.payment_status.create_payment_status_dto import CreatePaymentStatusDTO
from src.core.domain.dtos.payment_status.payment_status_dto import PaymentStatusDTO


class IPaymentStatusService(ABC):

    @abstractmethod
    def get_payment_status_by_name(self, name: str) -> PaymentStatusDTO:
        pass

    @abstractmethod
    def get_payment_status_by_id(self, payment_status_id: int) -> PaymentStatusDTO:
        pass

    @abstractmethod
    def get_all_payment_status(self, include_deleted: Optional[bool]) -> List[PaymentStatusDTO]:
        pass

    @abstractmethod
    def update_payment_status(self, payment_status_id: int, dto: UpdatePaymentStatusDTO) -> PaymentStatusDTO:
        pass

    @abstractmethod
    def delete_payment_status(self, payment_status_id: int) -> None:
        pass


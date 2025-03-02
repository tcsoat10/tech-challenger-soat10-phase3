
from typing import List, Optional
from config.database import DELETE_MODE
from src.core.domain.dtos.payment_status.update_payment_status_dto import UpdatePaymentStatusDTO
from src.core.domain.entities.payment_status import PaymentStatus
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository
from src.core.domain.dtos.payment_status.create_payment_status_dto import CreatePaymentStatusDTO
from src.core.domain.dtos.payment_status.payment_status_dto import PaymentStatusDTO
from src.core.ports.payment_status.i_payment_status_service import IPaymentStatusService


class PaymentStatusService(IPaymentStatusService):

    def __init__(self, payment_status_repository: IPaymentStatusRepository):
        self.repoistory = payment_status_repository
    
    def delete_payment_status(self, payment_status_id: int) -> None:
        payment_status = self.repoistory.get_by_id(payment_status_id)
        if not payment_status:
            raise EntityNotFoundException(entity_name="PaymentStatus")
        
        if DELETE_MODE == 'soft':
            if payment_status.is_deleted():
                raise EntityNotFoundException(entity_name="PaymentStatus")

            payment_status.soft_delete()
            self.repoistory.update(payment_status)
        else:
            self.repoistory.delete(payment_status)

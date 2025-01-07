
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

    def create_payment_status(self, dto: CreatePaymentStatusDTO) -> PaymentStatusDTO:
        payment_status = self.repoistory.get_by_name(dto.name)
        
        if payment_status:
            if not payment_status.is_deleted():
                raise EntityDuplicatedException(entity_name="PaymentStatus")
            
            payment_status.name = dto.name
            payment_status.description = dto.description
            payment_status.reactivate()
            self.repoistory.update(payment_status)
        else:
            payment_status = PaymentStatus(name=dto.name, description=dto.description)
            payment_status = self.repoistory.create(payment_status)

        return PaymentStatusDTO.from_entity(payment_status)
    
    def get_payment_status_by_name(self, name: str) -> PaymentStatusDTO:
        payment_status = self.repoistory.get_by_name(name=name)
        if not payment_status:
            raise EntityNotFoundException(entity_name="PaymentStatus")
        
        return PaymentStatusDTO.from_entity(payment_status)

    def get_payment_status_by_id(self, payment_status_id: int) -> PaymentStatusDTO:
        payment_status = self.repoistory.get_by_id(payment_status_id)
        if not payment_status:
            raise EntityNotFoundException(entity_name="PaymentStatus")
        
        return PaymentStatusDTO.from_entity(payment_status)
    
    def get_all_payment_status(self, include_deleted: Optional[bool] = False) -> List[PaymentStatusDTO]:
        payment_status = self.repoistory.get_all(include_deleted=include_deleted)
        return [PaymentStatusDTO.from_entity(payment_status) for payment_status in payment_status]
    
    def update_payment_status(self, payment_status_id: int, dto: UpdatePaymentStatusDTO) -> PaymentStatusDTO:
        payment_status = self.repoistory.get_by_id(payment_status_id)
        if not payment_status:
            raise EntityNotFoundException(entity_name="PaymentStatus")
        
        payment_status.name = dto.name
        payment_status.description = dto.description
        updated_payment_status = self.repoistory.update(payment_status)

        return PaymentStatusDTO.from_entity(updated_payment_status)
    
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

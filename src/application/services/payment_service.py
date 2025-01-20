from src.core.ports.payment.i_payment_service import IPaymentService
from src.core.ports.payment.i_payment_repository import IPaymentRepository
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository
from src.core.domain.dtos.payment.create_payment_dto import CreatePaymentDTO
from src.core.domain.dtos.payment.payment_dto import PaymentDTO
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.domain.entities.payment import Payment
from src.core.domain.dtos.payment.update_payment_dto import UpdatePaymentDTO

from typing import List


class PaymentService(IPaymentService):
    def __init__(
            self,
            repository: IPaymentRepository,
            payment_method_repository: IPaymentMethodRepository,
            payment_status_repository: IPaymentStatusRepository
    ):
        self.repository = repository
        self.method_repository = payment_method_repository
        self.status_repository = payment_status_repository
    
    def create_payment(self, dto: CreatePaymentDTO) -> PaymentDTO:
        payment_method = self.method_repository.get_by_id(dto.payment_method_id)
        if not payment_method:
            raise EntityNotFoundException(entity_name='Payment Method')
        
        payment_status = self.status_repository.get_by_id(dto.payment_status_id)
        if not payment_status:
            raise EntityNotFoundException(entity_name='Payment Status')
        
        payment = Payment(payment_method=payment_method, payment_status=payment_status)
        payment = self.repository.create(payment)

        return PaymentDTO.from_entity(payment)
    
    def get_payment_by_id(self, payment_id: int) -> PaymentDTO:
        payment = self.repository.get_by_id(payment_id)
        if not payment:
            raise EntityNotFoundException(entity_name='Payment')
        return PaymentDTO.from_entity(payment)
    
    def get_payments_by_method_id(self, method_id: int) -> List[PaymentDTO]:
        payments = self.repository.get_by_method_id(method_id)
        return [PaymentDTO.from_entity(payment) for payment in payments]
    
    def get_payments_by_status_id(self, status_id: int) -> List[PaymentDTO]:
        payments = self.repository.get_by_status_id(status_id)
        return [PaymentDTO.from_entity(payment) for payment in payments]
    
    def get_all_payments(self, include_deleted: bool = False) -> List[PaymentDTO]:
        payments = self.repository.get_all(include_deleted=include_deleted)
        return [PaymentDTO.from_entity(payment) for payment in payments]
    
    def update_payment(self, payment_id: int, dto: UpdatePaymentDTO) -> PaymentDTO:
        payment = self.repository.get_by_id(payment_id)
        if not payment:
            raise EntityNotFoundException(entity_name='Payment')
        
        method = self.method_repository.get_by_id(dto.payment_method_id)
        if not method:
            raise EntityNotFoundException(entity_name='Payment Method')
        
        status = self.status_repository.get_by_id(dto.payment_status_id)
        if not status:
            raise EntityNotFoundException(entity_name='Payment Status')
        
        payment.payment_method = method
        payment.payment_status = status

        payment = self.repository.update(payment)

        return PaymentDTO.from_entity(payment)
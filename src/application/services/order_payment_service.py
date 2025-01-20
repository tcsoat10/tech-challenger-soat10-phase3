from src.core.ports.order_payment.i_order_payment_service import IOrderPaymentService
from src.core.ports.order_payment.i_order_payment_repository import IOrderPaymentRepository
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.payment.i_payment_repository import IPaymentRepository
from src.core.domain.dtos.order_payment.create_order_payment_dto import CreateOrderPaymentDTO
from src.core.domain.dtos.order_payment.order_payment_dto import OrderPaymentDTO
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.domain.entities.order_payment import OrderPayment
from src.core.domain.dtos.order_payment.update_order_payment_dto import UpdateOrderPaymentDTO
from config.database import DELETE_MODE

from typing import List


class OrderPaymentService(IOrderPaymentService):
    def __init__(
            self,
            repository: IOrderPaymentRepository,
            order_repository: IOrderRepository,
            payment_repository: IPaymentRepository
    ):
        self.repository = repository
        self.order_repository = order_repository
        self.payment_repository = payment_repository

    def create_order_payment(self, dto: CreateOrderPaymentDTO) -> OrderPaymentDTO:
        order = self.order_repository.get_by_id(dto.order_id)
        if not order:
            raise EntityNotFoundException(entity_name='Order')
        
        payment = self.payment_repository.get_by_id(dto.payment_id)
        if not payment:
            raise EntityNotFoundException(entity_name='Payment')
        
        order_payment = OrderPayment(order=order, payment=payment)
        order_payment = self.repository.create(order_payment)

        return OrderPaymentDTO.from_entity(order_payment)
    
    def get_order_payment_by_id(self, order_payment_id: int) -> OrderPaymentDTO:
        order_payment = self.repository.get_by_id(order_payment_id)
        if not order_payment:
            raise EntityNotFoundException(entity_name='Order Payment')
        return OrderPaymentDTO.from_entity(order_payment)
    
    def get_order_payment_by_order_id(self, order_id: int) -> OrderPaymentDTO:
        order_payment = self.repository.get_by_order_id(order_id)
        if not order_payment:
            raise EntityNotFoundException(entity_name='Order Payment')
        return OrderPaymentDTO.from_entity(order_payment)
        
    def get_order_payment_by_payment_id(self, payment_id: int) -> OrderPaymentDTO:
        order_payment = self.repository.get_by_payment_id(payment_id)
        if not order_payment:
            raise EntityNotFoundException(entity_name='Order Payment')
        return OrderPaymentDTO.from_entity(order_payment)
    
    def get_all_order_payments(self, include_deleted: bool = False) -> List[OrderPaymentDTO]:
        order_payments = self.repository.get_all(include_deleted=include_deleted)
        return [OrderPaymentDTO.from_entity(order_payment) for order_payment in order_payments]
    
    def update_order_payment(self, dto: UpdateOrderPaymentDTO) -> OrderPaymentDTO:
        order_payment = self.repository.get_by_id(dto.id)
        if not order_payment:
            raise EntityNotFoundException(entity_name='Order Payment')
        
        order = self.order_repository.get_by_id(dto.order_id)
        if not order:
            raise EntityNotFoundException(entity_name='Order')
        
        payment = self.payment_repository.get_by_id(dto.payment_id)
        if not payment:
            raise EntityNotFoundException(entity_name='Payment')
        
        order_payment.order = order
        order_payment.payment = payment

        order_payment = self.repository.update(order_payment)

        return OrderPaymentDTO.from_entity(order_payment)
    
    def delete_order_payment(self, order_payment_id: int) -> None:
        order_payment = self.repository.get_by_id(order_payment_id)
        if not order_payment:
            raise EntityNotFoundException(entity_name='Order Payment')
        
        if DELETE_MODE == 'soft':
            if order_payment.is_deleted():
                raise EntityNotFoundException(entity_name='Order Payment')
            order_payment.soft_delete()
            self.repository.update(order_payment)
        else:
            self.repository.delete(order_payment_id)
            
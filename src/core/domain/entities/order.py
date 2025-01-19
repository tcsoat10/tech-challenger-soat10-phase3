from typing import List, Optional
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from core.domain.entities.employee import Employee
from core.domain.entities.order_status import OrderStatus
from core.domain.entities.order_item import OrderItem
from src.core.exceptions.bad_request_exception import BadRequestException
from src.constants.order_status import OrderStatusEnum
from .base_entity import BaseEntity

STATUS_TRANSITIONS = {
    OrderStatusEnum.ORDER_PENDING: OrderStatusEnum.ORDER_PLACED,
    OrderStatusEnum.ORDER_PLACED: OrderStatusEnum.ORDER_PREPARING,
    OrderStatusEnum.ORDER_PREPARING: OrderStatusEnum.ORDER_READY,
    OrderStatusEnum.ORDER_READY: OrderStatusEnum.ORDER_COMPLETED,
}

class Order(BaseEntity):
    __tablename__ = 'orders'

    id_customer = Column('id_customer', Integer, ForeignKey('customers.id'), nullable=False)
    customer = relationship('Customer')
    id_order_status = Column('id_order_status', Integer, ForeignKey('order_status.id'), nullable=False, default=1)
    order_status = relationship('OrderStatus')
    id_employee = Column('id_employee', Integer, ForeignKey('employees.id'), nullable=True)
    employee = relationship('Employee')

    order_items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')

    @property
    def order_status_name(self) -> str:
        return self.order_status.status

    @property
    def customer_person(self) -> Optional[str]:
        return self.customer.person if self.customer else None

    @property
    def employee_name(self) -> Optional[str]:
        return self.employee.person.name if self.employee else None

    @property
    def total(self) -> float:
        if not hasattr(self, "_total"):
            self._total = sum(item.total for item in self.order_items)
        return self._total
    
    @property
    def is_paid(self) -> bool:
        # TODO: Implementar lógica para verificar se o pagamento foi realizado
        return True

    def _validate_status(self, valid_statuses: List[OrderStatusEnum], action: str) -> None:
        if self.order_status.status not in [status.status for status in valid_statuses]:
            raise BadRequestException(f"O pedido não está em um estado válido para {action}.")

    def _validate_new_status(self, new_status: OrderStatus, expected_status: OrderStatusEnum) -> None:
        if new_status.status != expected_status.status:
            raise BadRequestException(f"O status {new_status.status} é inválido. Esperado: {expected_status.status}.")

    def add_item(self, item: OrderItem) -> None:
        self._validate_status([OrderStatusEnum.ORDER_PENDING], "adicionar itens")
        self.order_items.append(item)

    def remove_item(self, item: OrderItem) -> None:
        self._validate_status([OrderStatusEnum.ORDER_PENDING], "remover itens")
        self.order_items.remove(item)

    def place_order(self, new_status: OrderStatus) -> None:
        self._validate_status([OrderStatusEnum.ORDER_PENDING], "realizar o pedido")
        self._validate_new_status(new_status, OrderStatusEnum.ORDER_PLACED)
        self.order_status = new_status

    def cancel_order(self, new_status: OrderStatus) -> None:
        self._validate_status([OrderStatusEnum.ORDER_PENDING, OrderStatusEnum.ORDER_PLACED], "cancelar o pedido")
        self._validate_new_status(new_status, OrderStatusEnum.ORDER_CANCELLED)
        self.order_status = new_status

    def prepare_order(self, employee: Employee, new_status: OrderStatus) -> None:
        self._validate_status([OrderStatusEnum.ORDER_PLACED], "preparar o pedido")
        self._validate_new_status(new_status, OrderStatusEnum.ORDER_PREPARING)
        
        if not self.is_paid:
            raise BadRequestException("O pedido ainda não foi pago. Não é possível preparar o pedido.")
        
        if not employee:
            raise BadRequestException("É necessário um funcionário para preparar o pedido.")

        self.id_employee = employee.id
        self.employee = employee
        self.order_status = new_status

    def mark_as_ready(self, new_status: OrderStatus) -> None:
        self._validate_status([OrderStatusEnum.ORDER_PREPARING], "finalizar o preparo do pedido")
        self._validate_new_status(new_status, OrderStatusEnum.ORDER_READY)
        self.order_status = new_status

    def complete_order(self, new_status: OrderStatus) -> None:
        self._validate_status([OrderStatusEnum.ORDER_READY], "completar o pedido")
        self._validate_new_status(new_status, OrderStatusEnum.ORDER_COMPLETED)
        self.order_status = new_status

    def next_step(self, new_status: Optional[OrderStatus] = None, employee: Optional[Employee] = None) -> None:
        current_status = OrderStatusEnum(self.order_status.status)

        if current_status not in STATUS_TRANSITIONS:
            raise BadRequestException(f"O estado atual {current_status.status} não permite transições.")

        expected_next_status = STATUS_TRANSITIONS[current_status]

        if expected_next_status == OrderStatusEnum.ORDER_PREPARING:
            if not self.is_paid:
                raise BadRequestException("O pedido ainda não foi pago. Não é possível preparar o pedido.")
            
            if not employee:
                raise BadRequestException("É necessário um funcionário para preparar o pedido.")

            self.id_employee = employee.id
            self.employee = employee

        if new_status:
            self._validate_new_status(new_status, expected_next_status)
            self.order_status = new_status
        else:
            self.order_status.status = expected_next_status.status

    __all__ = ['Order']

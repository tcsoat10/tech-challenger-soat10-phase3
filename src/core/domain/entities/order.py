from typing import Optional, TYPE_CHECKING
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.core.domain.entities.order_item import OrderItem
from src.core.exceptions.bad_request_exception import BadRequestException
from src.constants.order_status import OrderStatusEnum
from .base_entity import BaseEntity

if TYPE_CHECKING:
    from src.adapters.driven.repositories.order_repository import OrderRepository

# tabelas
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
    def order_status_name(self):
        return self.order_status.status

    @property
    def customer_person(self):
        return self.customer.person
    
    @property
    def employee_name(self):
        return self.employee.person.name
    
    @property
    def total(self):
        return sum([item.total for item in self.order_items])
    
    def add_item(self, item: OrderItem, repository: Optional['OrderRepository']) -> None:
        if self.order_status.status not in [OrderStatusEnum.ORDER_PENDING]:
            raise BadRequestException(message='Pedido não está pendente. Não é possível adicionar itens.')
        
        self.order_items.append(item)
        
        if repository:
            repository.update(self)

    def remove_item(self, item: OrderItem, repository: Optional['OrderRepository']) -> None:
        if self.order_status.status not in [OrderStatusEnum.ORDER_PENDING]:
            raise BadRequestException(message='Pedido não está pendente. Não é possível adicionar itens.')

        self.order_items.remove(item)

        if repository:
            repository.update(self)

    def place_order(self, repository: Optional['OrderRepository']) -> None:
        if self.order_status.status not in [OrderStatusEnum.ORDER_PENDING]:
            raise BadRequestException(message='Pedido não está pendente. Não é possível realizar o pedido.')
        
        self.order_status = OrderStatusEnum.ORDER_PLACED
        
        if repository:
            repository.update(self)

    def cancel_order(self, repository: Optional['OrderRepository']) -> None:
        # TODO: adicionar validação com status do pagamento. Caso o pagamento já tenha sido realizado, não é possível cancelar o pedido.
        if self.order_status.status not in [OrderStatusEnum.ORDER_PENDING, OrderStatusEnum.ORDER_PLACED]:
            raise BadRequestException(message='Pedido não está pendente ou realizado. Não é possível cancelar o pedido.')
        
        self.order_status = OrderStatusEnum.ORDER_CANCELLED
        if repository:
            repository.update(self)
    
    def prepare_order(self, repository: Optional['OrderRepository']) -> None:
        # TODO: adicionar validação com status do pagamento. Se não houver pagamento, não é possível preparar o pedido.
        if self.order_status.status not in [OrderStatusEnum.ORDER_PLACED]:
            raise BadRequestException(message='Pedido não está realizado. Não é possível preparar o pedido.')
        
        self.order_status = OrderStatusEnum.ORDER_PREPARING
        
        if repository:
            repository.update(self)
    
    def ready_order(self, repository: Optional['OrderRepository']) -> None:
        if self.order_status.status not in [OrderStatusEnum.ORDER_PREPARING]:
            raise BadRequestException(message='Pedido não está sendo preparado. Não é possível finalizar o pedido.')
        
        self.order_status = OrderStatusEnum.ORDER_READY
        repository.update(self)

    def complete_order(self, repository: Optional['OrderRepository']) -> None:
        if self.order_status.status not in [OrderStatusEnum.ORDER_READY]:
            raise BadRequestException(message='Pedido não está pronto. Não é possível finalizar o pedido.')
        
        self.order_status = OrderStatusEnum.ORDER_COMPLETED
        
        if repository:
            repository.update(self)

    __all__ = ['Order']
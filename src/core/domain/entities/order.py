from typing import Optional, TYPE_CHECKING
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.core.domain.entities.order_item import OrderItem
from src.core.exceptions.bad_request_exception import BadRequestException
from src.constants.order_status import OrderStatusEnum
from .base_entity import BaseEntity

if TYPE_CHECKING:
    from src.core.ports.order.i_order_repository import IOrderRepository

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
    
    def add_item(self, item: OrderItem, repository: Optional['IOrderRepository']) -> None:
        if self.order_status.status not in [OrderStatusEnum.ORDER_PENDING.status]:
            raise BadRequestException(message='Pedido não está pendente. Não é possível adicionar itens.')
        
        self.order_items.append(item)
        
        if repository:
            repository.update(self)

    def remove_item(self, item: OrderItem, repository: Optional['IOrderRepository']) -> None:
        if self.order_status.status not in [OrderStatusEnum.ORDER_PENDING.status]:
            raise BadRequestException(message='Pedido não está pendente. Não é possível adicionar itens.')

        self.order_items.remove(item)

        if repository:
            repository.update(self)

    def place_order(self, order_status_repository: IOrderStatusRepository, repository: Optional['IOrderRepository']) -> None:
        if self.order_status.status not in [OrderStatusEnum.ORDER_PENDING.status]:
            raise BadRequestException(message='Pedido não está pendente. Não é possível realizar o pedido.')
        
        order_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_PLACED.status)
        self.order_status = order_status
        
        if repository:
            repository.update(self)

    def cancel_order(self, order_status_repository: IOrderStatusRepository, repository: Optional['IOrderRepository']) -> None:
        # TODO: adicionar validação com status do pagamento. Caso o pagamento já tenha sido realizado, não é possível cancelar o pedido.
        if self.order_status.status not in [OrderStatusEnum.ORDER_PENDING.status, OrderStatusEnum.ORDER_PLACED.status]:
            raise BadRequestException(message='Pedido não está pendente ou realizado. Não é possível cancelar o pedido.')
        
        order_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_CANCELLED.status)
        self.order_status = order_status
        
        if repository:
            repository.update(self)
    
    def prepare_order(self, order_status_repository: IOrderStatusRepository, repository: Optional['IOrderRepository']) -> None:
        # TODO: adicionar validação com status do pagamento. Se não houver pagamento, não é possível preparar o pedido.
        if self.order_status.status not in [OrderStatusEnum.ORDER_PLACED.status]:
            raise BadRequestException(message='Pedido não está realizado. Não é possível preparar o pedido.')
        
        order_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_PREPARING.status)
        self.order_status = order_status
        
        if repository:
            repository.update(self)
    
    def ready_order(self, order_status_repository: IOrderStatusRepository, repository: Optional['IOrderRepository']) -> None:
        if self.order_status.status not in [OrderStatusEnum.ORDER_PREPARING.status]:
            raise BadRequestException(message='Pedido não está sendo preparado. Não é possível finalizar o pedido.')
        
        order_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_READY.status)
        self.order_status = order_status
        
        if repository:
            repository.update(self)

    def complete_order(self, order_status_repository: IOrderStatusRepository, repository: Optional['IOrderRepository']) -> None:
        if self.order_status.status not in [OrderStatusEnum.ORDER_READY.status]:
            raise BadRequestException(message='Pedido não está pronto. Não é possível finalizar o pedido.')
        
        order_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_COMPLETED.status)
        self.order_status = order_status
        
        if repository:
            repository.update(self)

    __all__ = ['Order']
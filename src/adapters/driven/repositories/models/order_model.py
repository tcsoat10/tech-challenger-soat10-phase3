from typing import List
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.adapters.driven.repositories.models.base_model import BaseModel
from src.adapters.driven.repositories.models.order_item_model import OrderItemModel
from src.adapters.driven.repositories.models.order_status_movement_model import OrderStatusMovementModel
from src.core.domain.entities.order import Order
from src.core.domain.entities.order_item import OrderItem
from src.core.shared.identity_map import IdentityMap


class OrderModel(BaseModel):
    __tablename__ = 'orders'

    id_customer = Column('id_customer', Integer, ForeignKey('customers.id'), nullable=False)
    customer = relationship('CustomerModel')

    id_order_status = Column('id_order_status', Integer, ForeignKey('order_status.id'), nullable=False, default=1)
    order_status = relationship('OrderStatusModel')

    id_employee = Column('id_employee', Integer, ForeignKey('employees.id'), nullable=True)
    employee = relationship('EmployeeModel')

    id_payment = Column(ForeignKey('payments.id'), nullable=True)
    payment = relationship('PaymentModel', back_populates='order')

    order_items = relationship('OrderItemModel', back_populates='order', cascade='all, delete-orphan')

    status_history = relationship(
        'OrderStatusMovementModel',
        back_populates='order',
        cascade='all, delete-orphan',
        order_by='OrderStatusMovementModel.changed_at',
    )
    
    @classmethod
    def from_entity(cls, order: Order) -> 'OrderModel':
        id_customer = order.customer.id if order.customer else None
        id_employee = order.employee.id if order.employee else None
        id_payment = order.payment.id if order.payment else None
        id_order_status = order.order_status.id if order.order_status else None
        
        return cls(
            id_customer=id_customer,
            id_order_status=id_order_status,
            id_employee=id_employee,
            id_payment=id_payment,
            order_items=[OrderItemModel.from_entity(order_item) for order_item in order.order_items],
            status_history=[OrderStatusMovementModel.from_entity(movement) for movement in order.status_history],
            id=order.id,
            created_at=order.created_at,
            updated_at=order.updated_at,
            inactivated_at=order.inactivated_at,
        )
        
    def to_entity(self) -> Order:
        identity_map: IdentityMap = IdentityMap.get_instance()
        if existing_order := identity_map.get(Order, self.id):
            return existing_order

        order = Order(id=self.id)
        identity_map.add(order)

        order.customer = self._get_customer(identity_map)
        order.order_status = self._get_order_status(identity_map)
        order.employee = self._get_employee(identity_map)
        order.order_items = self._get_order_items(identity_map)
        order.status_history = self._get_status_history(identity_map)
        order.created_at = self.created_at
        order.updated_at = self.updated_at
        order.inactivated_at = self.inactivated_at

        if self.payment:
            order.payment = self._get_payment(identity_map)

        return order
        
    def _get_order_items(self, identity_map: IdentityMap) -> List[OrderItem]:
        from src.core.domain.entities.order_item import OrderItem
        
        existing_items = []
        for item in self.order_items:
            if existing_item := identity_map.get(OrderItem, item.id):
                existing_items.append(existing_item)
            else:
                order_item = item.to_entity()
                identity_map.add(order_item)
                existing_items.append(order_item)
        
        if not existing_items:
            existing_items = [item.to_entity() for item in self.order_items]

        return existing_items
    
    def _get_status_history(self, identity_map: IdentityMap) -> list:
        from src.core.domain.entities.order import OrderStatusMovement
        
        existing_movements = []
        for movement in self.status_history:
            if existing_movement := identity_map.get(OrderStatusMovement, movement.id):
                existing_movements.append(existing_movement)
            else:
                order_status_movement = movement.to_entity()
                identity_map.add(order_status_movement)
                existing_movements.append(order_status_movement)
        
        if not existing_movements:
            existing_movements = [movement.to_entity() for movement in self.status_history]

        return existing_movements
    
    def _get_customer(self, identity_map: IdentityMap):
        from src.core.domain.entities.customer import Customer
        
        if existing_customer := identity_map.get(Customer, self.id_customer):
            return existing_customer
        return self.customer.to_entity()
    
    def _get_order_status(self, identity_map: IdentityMap):
        from src.core.domain.entities.order_status import OrderStatus
        
        if existing_order_status := identity_map.get(OrderStatus, self.id_order_status):
            return existing_order_status
        return self.order_status.to_entity()
    
    def _get_employee(self, identity_map: IdentityMap):
        from src.core.domain.entities.employee import Employee
        
        if existing_employee := identity_map.get(Employee, self.id_employee):
            return existing_employee
        return self.employee.to_entity() if self.employee else None
    
    def _get_payment(self, identity_map: IdentityMap):
        from src.core.domain.entities.payment import Payment
        
        if existing_payment := identity_map.get(Payment, self.id_payment):
            return existing_payment
        return self.payment.to_entity() if self.payment else None


__all__ = ['OrderModel']
    
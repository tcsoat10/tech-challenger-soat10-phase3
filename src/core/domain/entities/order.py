from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .base_entity import BaseEntity

# tabelas
class Order(BaseEntity):
    __tablename__ = 'orders'

    id_customer = Column('id_customer', Integer, ForeignKey('customers.id'), nullable=False)
    customer = relationship('Customer')
    id_order_status = Column('id_order_status', Integer, ForeignKey('order_status.id'), nullable=False)
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

    __all__ = ['Order']
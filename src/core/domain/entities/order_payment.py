from src.core.domain.entities.base_entity import BaseEntity

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship


class OrderPayment(BaseEntity):
    __tablename__ = 'order_payments'

    order_id = Column(ForeignKey('orders.id'), nullable=False)
    order = relationship('Order', back_populates='payments')

    payment_id = Column(ForeignKey('payments.id'), nullable=False)
    payment = relationship('Payment', back_populates='orders')


__all__ = ['OrderPayment']
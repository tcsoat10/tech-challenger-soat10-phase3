from src.core.domain.entities.base_entity import BaseEntity

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship


class Payment(BaseEntity):
    __tablename__ = 'payments'

    payment_method_id = Column(ForeignKey('payment_methods.id'), nullable=False)
    payment_method = relationship('PaymentMethod')

    payment_status_id = Column(ForeignKey('payment_status.id'), nullable=False)
    payment_status = relationship('PaymentStatus')


__all__ = ['Payment']

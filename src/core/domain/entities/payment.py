from src.core.domain.entities.base_entity import BaseEntity

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship


class Payment(BaseEntity):
    __tablename__ = 'payments'

    payment_method_id = Column(ForeignKey('payment_methods.id'), nullable=False)
    payment_method = relationship('PaymentMethod', back_populates='payments')

    payment_status_id = Column(ForeignKey('payment_status.id'), nullable=False)
    payment_status = relationship('PaymentStatus', back_populates='payments')
    
    order = relationship('Order', back_populates='payment')

    amount = Column(Float, nullable=False)
    external_reference = Column(String(500), nullable=False)



__all__ = ['Payment']

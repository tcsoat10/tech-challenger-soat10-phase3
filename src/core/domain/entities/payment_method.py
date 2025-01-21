from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.core.domain.entities.base_entity import BaseEntity


class PaymentMethod(BaseEntity):

    __tablename__ = "payment_methods"

    name = Column(String(300), nullable=False, unique=True)
    description = Column(String(300), nullable=False)

    payments = relationship('Payment', back_populates='payment_method')

__all__ = ["PaymentMethod"]
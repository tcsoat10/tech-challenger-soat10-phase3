
from sqlalchemy import Column, String
from src.core.domain.entities.base_entity import BaseEntity


class PaymentStatus(BaseEntity):
    __tablename__ = 'payment_status'

    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255), nullable=True)



__all__ = ["PaymentStatus"]
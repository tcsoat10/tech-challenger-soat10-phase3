
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.core.shared.identity_map import IdentityMap
from src.core.domain.entities.payment_status import PaymentStatus
from src.adapters.driven.repositories.models.base_model import BaseModel


class PaymentStatusModel(BaseModel):
    __tablename__ = 'payment_status'

    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255), nullable=True)

    payments = relationship('PaymentModel', back_populates='payment_status')

    @classmethod
    def from_entity(cls, payment_status: PaymentStatus):
        return cls(
            name=payment_status.name,
            description=payment_status.description,
            id=payment_status.id,
            created_at=payment_status.created_at,
            updated_at=payment_status.updated_at,
            inactivated_at=payment_status.inactivated_at
        )
        
    def to_entity(self) -> PaymentStatus:
        identity_map: IdentityMap = IdentityMap.get_instance()
        existing_entity = identity_map.get(PaymentStatus, self.id)
        if existing_entity:
            return existing_entity
        
        payment_status = PaymentStatus(
            name=self.name,
            description=self.description
        )
        identity_map.add(payment_status)
        
        payment_status.payments = [payment.to_entity() for payment in self.payments]
        payment_status.id = self.id
        payment_status.created_at = self.created_at
        payment_status.updated_at = self.updated_at
        payment_status.inactivated_at = self.inactivated_at
        
        return payment_status
        

__all__ = ["PaymentStatusModel"]

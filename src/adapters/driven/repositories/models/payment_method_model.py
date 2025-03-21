from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.adapters.driven.repositories.models.base_model import BaseModel
from src.core.domain.entities.payment_method import PaymentMethod
from src.core.shared.identity_map import IdentityMap


class PaymentMethodModel(BaseModel):

    __tablename__ = "payment_methods"

    name = Column(String(300), nullable=False, unique=True)
    description = Column(String(300), nullable=False)

    payments = relationship('PaymentModel', back_populates='payment_method')
    
    @classmethod
    def from_entity(cls, entity: PaymentMethod) -> "PaymentMethodModel":
        return cls(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            inactivated_at=entity.inactivated_at
        )
        
    def to_entity(self) -> PaymentMethod:
        identity_map: IdentityMap = IdentityMap.get_instance()
        existing_entity: PaymentMethod = identity_map.get(PaymentMethod, self.id)
        if existing_entity:
            return existing_entity
        
        payment_method = PaymentMethod(
            id=self.id,
            name=self.name,
            description=self.description,
        )
        identity_map.add(payment_method)

        payment_method.payments = [payment.to_entity() for payment in self.payments]
        payment_method.created_at = self.created_at
        payment_method.updated_at = self.updated_at
        payment_method.inactivated_at = self.inactivated_at
        
        return payment_method

__all__ = ["PaymentMethodModel"]

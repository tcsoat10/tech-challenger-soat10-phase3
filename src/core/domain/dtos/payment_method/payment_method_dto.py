
from pydantic import BaseModel

from src.core.domain.entities.payment_method import PaymentMethod


class PaymentMethodDTO(BaseModel):
    id: int
    name: str
    description: str

    @classmethod
    def from_entity(cls, payment_method: PaymentMethod) -> "PaymentMethodDTO":
        return cls(id=payment_method.id, name=payment_method.name, description=payment_method.description)

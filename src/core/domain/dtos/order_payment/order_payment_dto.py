from pydantic import BaseModel

from src.core.domain.dtos.order.order_dto import OrderDTO
from src.core.domain.dtos.payment.payment_dto import PaymentDTO
from src.core.domain.entities.order_payment import OrderPayment


class OrderPaymentDTO(BaseModel):
    id: int
    order: OrderDTO
    payment: PaymentDTO

    @classmethod
    def from_entity(cls, order_payment: OrderPayment) -> 'OrderPaymentDTO':
        return cls(
            id=order_payment.id,
            order=OrderDTO.from_entity(order_payment.order),
            payment=PaymentDTO.from_entity(order_payment.payment)
        )
    
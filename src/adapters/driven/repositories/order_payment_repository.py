from src.core.ports.order_payment.i_order_payment_repository import IOrderPaymentRepository
from src.core.domain.entities.order_payment import OrderPayment

from sqlalchemy.orm import Session


class OrderPaymentRepository(IOrderPaymentRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, order_payment: OrderPayment) -> OrderPayment:
        self.db_session.add(order_payment)
        self.db_session.commit()
        self.db_session.refresh(order_payment)
        return order_payment
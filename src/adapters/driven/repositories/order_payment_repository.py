from src.core.ports.order_payment.i_order_payment_repository import IOrderPaymentRepository
from src.core.domain.entities.order_payment import OrderPayment
from src.core.domain.entities.order import Order
from src.core.domain.entities.payment import Payment

from sqlalchemy.orm import Session


class OrderPaymentRepository(IOrderPaymentRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, order_payment: OrderPayment) -> OrderPayment:
        self.db_session.add(order_payment)
        self.db_session.commit()
        self.db_session.refresh(order_payment)
        return order_payment
    
    def get_by_id(self, order_payment_id: int) -> OrderPayment:
        return self.db_session.query(OrderPayment).filter(OrderPayment.id == order_payment_id).first()
    
    def get_by_order_id(self, order_id: int) -> OrderPayment:
        return self.db_session.query(OrderPayment).join(OrderPayment.order).filter(Order.id == order_id).first()
    
    def get_by_payment_id(self, payment_id: int) -> OrderPayment:
        return self.db_session.query(OrderPayment).join(OrderPayment.payment).filter(Payment.id == payment_id).first()

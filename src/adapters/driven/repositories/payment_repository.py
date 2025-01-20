from src.core.ports.payment.i_payment_repository import IPaymentRepository
from src.core.domain.entities.payment import Payment
from src.core.domain.entities.payment_method import PaymentMethod

from sqlalchemy.orm import Session
from typing import List


class PaymentRepository(IPaymentRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, payment: Payment) -> Payment:
        self.db_session.add(payment)
        self.db_session.commit()
        self.db_session.refresh(payment)
        return payment

    def get_by_id(self, payment_id: int) -> Payment:
        return self.db_session.query(Payment).filter(Payment.id == payment_id).first()
    
    def get_by_method_id(self, method_id: int) -> List[Payment]:
        return self.db_session.query(Payment).join(Payment.payment_method).filter(PaymentMethod.id == method_id).all()
from src.core.ports.payment.i_payment_repository import IPaymentRepository
from src.core.domain.entities.payment import Payment
from src.core.domain.entities.payment_method import PaymentMethod
from src.core.domain.entities.payment_status import PaymentStatus

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
    
    def get_by_status_id(self, status_id: int) -> List[Payment]:
        return self.db_session.query(Payment).join(Payment.payment_status).filter(PaymentStatus.id == status_id).all()
    
    def get_all(self, include_deleted: bool = False) -> List[Payment]:
        query = self.db_session.query(Payment)
        if not include_deleted:
            query = query.filter(Payment.inactivated_at.is_(None))
        return query.all()
    
    def update(self, payment: Payment) -> Payment:
        self.db_session.merge(payment)
        self.db_session.commit()
        return payment
    
    def delete(self, payment_id: int) -> None:
        payment = self.get_by_id(payment_id)
        if payment:
            self.db_session.delete(payment)
            self.db_session.commit()

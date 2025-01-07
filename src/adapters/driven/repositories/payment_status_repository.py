from sqlalchemy.orm import Session

from src.core.domain.entities.payment_status import PaymentStatus
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository

class PaymentStatusRepository(IPaymentStatusRepository):

    def __init__(self, session: Session):
        self.session = session

    def create(self, payment_status):
        self.session.add(payment_status)
        self.session.commit()
        self.session.refresh(payment_status)
        return payment_status
    
    def exists_by_name(self, name):
        return self.session.query(self.session.query(PaymentStatus).filter(PaymentStatus.name == name).exists()).scalar()
    
    def get_by_name(self, name):
        return self.session.query(PaymentStatus).filter(PaymentStatus.name == name).first()
    
    def get_by_id(self, payment_status_id):
        return self.session.query(PaymentStatus).filter(PaymentStatus.id == payment_status_id).first()
    
    def get_all(self, include_deleted: bool = False):
        query = self.session.query(PaymentStatus)
        if not include_deleted:
            query = query.filter(PaymentStatus.inactivated_at.is_(None))
        return query.all()
    
    def update(self, payment_status):
        self.session.merge(payment_status)
        self.session.commit()
        return payment_status
    
    def delete(self, payment_status):
        self.session.delete(payment_status)
        self.session.commit()
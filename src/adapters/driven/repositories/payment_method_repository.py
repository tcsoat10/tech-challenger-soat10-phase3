from typing import Optional
from sqlalchemy import exists
from sqlalchemy.orm import Session

from src.core.domain.entities.payment_method import PaymentMethod
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository


class PaymentMethodRepository(IPaymentMethodRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, payment_method) -> PaymentMethod:
        self.db_session.add(payment_method)
        self.db_session.commit()
        self.db_session.refresh(payment_method)
        return payment_method
    
    def exists_by_name(self, name: str) -> bool:
        return self.db_session.query(exists().where(PaymentMethod.name == name)).scalar()
    
    def get_by_name(self, name: str) -> PaymentMethod:
        return self.db_session.query(PaymentMethod).filter(PaymentMethod.name == name).first()
    
    def get_by_id(self, payment_method_id: int) -> PaymentMethod:
        return self.db_session.query(PaymentMethod).get(payment_method_id)
    
    def get_all(self, include_deleted: Optional[bool] = False) -> list[PaymentMethod]:
        query = self.db_session.query(PaymentMethod)
        if not include_deleted:
            query = query.filter(PaymentMethod.inactivated_at.is_(None))
        return query.all()
    
    def update(self, payment_method) -> PaymentMethod:
        self.db_session.merge(payment_method)
        self.db_session.commit()
        return payment_method
    
    def delete(self, payment_method) -> None:
        self.db_session.delete(payment_method)
        self.db_session.commit()

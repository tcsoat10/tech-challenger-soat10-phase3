from typing import Optional
from sqlalchemy import exists
from sqlalchemy.orm import Session

from src.adapters.driven.repositories.models.payment_method_model import PaymentMethodModel
from src.core.shared.identity_map import IdentityMap
from src.core.domain.entities.payment_method import PaymentMethod
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository


class PaymentMethodRepository(IPaymentMethodRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.identity_map: IdentityMap = IdentityMap.get_instance()

    def create(self, payment_method: PaymentMethod) -> PaymentMethod:
        if payment_method.id is not None:
            existing_entity = self.identity_map.get(PaymentMethod, payment_method.id)
            if existing_entity:
                self.identity_map.remove(existing_entity)
        
        payment_method_model = PaymentMethodModel.from_entity(payment_method)
        self.db_session.add(payment_method_model)
        self.db_session.commit()
        self.db_session.refresh(payment_method_model)
        return payment_method_model.to_entity()
    
    def exists_by_name(self, name: str) -> bool:
        return self.db_session.query(exists().where(PaymentMethodModel.name == name)).scalar()
    
    def get_by_name(self, name: str) -> PaymentMethod:
        payment_method_model = self.db_session.query(PaymentMethodModel).filter(PaymentMethodModel.name == name).first()
        if payment_method_model is None:
            return None
        return payment_method_model.to_entity()
    
    def get_by_id(self, payment_method_id: int) -> PaymentMethod:
        payment_method_model = self.db_session.query(PaymentMethodModel).get(payment_method_id)
        if payment_method_model is None:
            return None
        return payment_method_model.to_entity()
    
    def get_all(self, include_deleted: Optional[bool] = False) -> list[PaymentMethod]:
        query = self.db_session.query(PaymentMethodModel)
        if not include_deleted:
            query = query.filter(PaymentMethodModel.inactivated_at.is_(None))
        payment_method_models = query.all()
        return [payment_method_model.to_entity() for payment_method_model in payment_method_models]
    
    def update(self, payment_method) -> PaymentMethod:
        if payment_method.id is not None:
            existing_entity = self.identity_map.get(PaymentMethod, payment_method.id)
            if existing_entity:
                self.identity_map.remove(existing_entity)
        
        payment_method_model = PaymentMethodModel.from_entity(payment_method)
        self.db_session.merge(payment_method_model)
        self.db_session.commit()
        return payment_method_model.to_entity()
    
    def delete(self, payment_method) -> None:
        payment_method_model = (
            self.db_session.query(PaymentMethodModel)
                .filter(PaymentMethodModel.id == payment_method.id)
                .first()
        )
        if payment_method_model:
            self.db_session.delete(payment_method)
            self.db_session.commit()
            self.identity_map.remove(payment_method)

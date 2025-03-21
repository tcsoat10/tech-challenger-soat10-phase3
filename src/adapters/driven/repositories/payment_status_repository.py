from sqlalchemy.orm import Session

from src.adapters.driven.repositories.models.payment_status_model import PaymentStatusModel
from src.core.shared.identity_map import IdentityMap
from src.core.domain.entities.payment_status import PaymentStatus
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository

class PaymentStatusRepository(IPaymentStatusRepository):

    def __init__(self, session: Session):
        self.session = session
        self.identity_map: IdentityMap = IdentityMap.get_instance()

    def create(self, payment_status: PaymentStatus) -> PaymentStatus:
        if payment_status.id is not None:
            existing_entity = self.identity_map.get(PaymentStatus, payment_status)
            if existing_entity:
                self.identity_map.remove(existing_entity)
        
        payment_status_model = PaymentStatusModel.from_entity(payment_status)
        self.session.add(payment_status_model)
        self.session.commit()
        self.session.refresh(payment_status_model)
        return payment_status_model.to_entity()
    
    def exists_by_name(self, name):
        return self.session.query(self.session.query(PaymentStatusModel).filter(PaymentStatusModel.name == name).exists()).scalar()
    
    def get_by_name(self, name):
        payment_status_model = self.session.query(PaymentStatusModel).filter(PaymentStatusModel.name == name).first()
        if not payment_status_model:
            return None
        return payment_status_model.to_entity()
    
    def get_by_id(self, payment_status_id):
        payment_status_model = self.session.query(PaymentStatusModel).filter(PaymentStatusModel.id == payment_status_id).first()
        if not payment_status_model:
            return None
        return payment_status_model.to_entity()
    
    def get_all(self, include_deleted: bool = False):
        query = self.session.query(PaymentStatusModel)
        if not include_deleted:
            query = query.filter(PaymentStatusModel.inactivated_at.is_(None))
        payment_status_models = query.all()
        return [payment_status_model.to_entity() for payment_status_model in payment_status_models]
    
    def update(self, payment_status: PaymentStatus):
        if payment_status.id is not None:
            existing_entity = self.identity_map.get(PaymentStatus, payment_status)
            if existing_entity:
                self.identity_map.remove(existing_entity)

        payment_status_model = PaymentStatusModel.from_entity(payment_status)
        self.session.merge(payment_status_model)
        self.session.commit()
        return payment_status_model.to_entity()
    
    def delete(self, payment_status: PaymentStatus):
        payment_status_model = (
            self.session.query(PaymentStatusModel)
                .filter(PaymentStatusModel.id == payment_status.id)
                .first()
        )
        if payment_status_model:
            self.session.delete(payment_status_model)
            self.session.commit()
            self.identity_map.remove(payment_status)

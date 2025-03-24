from src.adapters.driven.repositories.models.order_model import OrderModel
from src.adapters.driven.repositories.models.base_model import BaseModel
from src.core.domain.entities.payment import Payment
from src.core.shared.identity_map import IdentityMap
from src.core.domain.entities.base_entity import BaseEntity

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship


class PaymentModel(BaseModel):
    __tablename__ = 'payments'

    payment_method_id = Column(ForeignKey('payment_methods.id'), nullable=False)
    payment_method = relationship('PaymentMethodModel', back_populates='payments')

    payment_status_id = Column(ForeignKey('payment_status.id'), nullable=False)
    payment_status = relationship('PaymentStatusModel', back_populates='payments')
    
    order = relationship('OrderModel', back_populates='payment')

    amount = Column(Float, nullable=False)
    external_reference = Column(String(500), nullable=False)

    qr_code = Column(String(500), nullable=True)
    transaction_id = Column(String(100), nullable=True)
    
    @classmethod
    def from_entity(cls, payment: BaseEntity):
        payment_method_id = payment.payment_method.id if payment.payment_method else None
        payment_status_id = payment.payment_status.id if payment.payment_status else None
        order_model = [OrderModel.from_entity(order_model) for order_model in payment.order] if payment.order else []

        return cls(
            payment_method_id=payment_method_id,
            payment_status_id=payment_status_id,
            amount=payment.amount,
            order=order_model,
            external_reference=payment.external_reference,
            qr_code=payment.qr_code,
            transaction_id=payment.transaction_id,
            id=payment.id,
            created_at=payment.created_at,
            updated_at=payment.updated_at,
            inactivated_at=payment.inactivated_at
        )
    
    def to_entity(self) -> Payment:
        identity_map: IdentityMap = IdentityMap.get_instance()
        existing_payment = identity_map.get(Payment, self.id)
        if existing_payment:
            return existing_payment

        payment = Payment(
            id=self.id,
            amount=self.amount,
            external_reference=self.external_reference,
            qr_code=self.qr_code,
            transaction_id=self.transaction_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            inactivated_at=self.inactivated_at,
        )
        identity_map.add(payment)

        payment.payment_method = self._get_payment_method(identity_map)
        payment.payment_status = self._get_payment_status(identity_map)

        if self.order:
            payment.order = [order_model.to_entity() for order_model in self.order]

        return payment
    
    def _get_payment_status(self, identity_map: IdentityMap):
        from src.core.domain.entities.payment_status import PaymentStatus
        payment_status = identity_map.get(PaymentStatus, self.payment_status_id)
        if payment_status:
            return payment_status
        
        return self.payment_status.to_entity()
    
    def _get_payment_method(self, identity_map: IdentityMap):
        from src.core.domain.entities.payment_method import PaymentMethod
        payment_method = identity_map.get(PaymentMethod, self.payment_method_id)
        if payment_method:
            return payment_method
        
        return self.payment_method.to_entity()
    

__all__ = ['PaymentModel']

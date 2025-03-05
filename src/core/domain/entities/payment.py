from src.core.ports.payment.i_payment_provider_gateway import IPaymentProviderGateway
from src.constants.payment_status import PaymentStatusEnum
from src.core.domain.entities.base_entity import BaseEntity

from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from typing import Dict, Any


class Payment(BaseEntity):
    __tablename__ = 'payments'

    payment_method_id = Column(ForeignKey('payment_methods.id'), nullable=False)
    payment_method = relationship('PaymentMethod', back_populates='payments')

    payment_status_id = Column(ForeignKey('payment_status.id'), nullable=False)
    payment_status = relationship('PaymentStatus', back_populates='payments')
    
    order = relationship('Order', back_populates='payment')

    amount = Column(Float, nullable=False)
    external_reference = Column(String(500), nullable=False)

    qr_code = Column(String(500), nullable=True)
    transaction_id = Column(String(100), nullable=True)
    
    def is_pending(self) -> bool:
        return self.payment_status.name == PaymentStatusEnum.PAYMENT_PENDING.status

    def is_completed(self) -> bool:
        return self.payment_status.name == PaymentStatusEnum.PAYMENT_COMPLETED.status
    
    def is_cancelled(self) -> bool:
        return self.payment_status.name == PaymentStatusEnum.PAYMENT_CANCELLED.status

    def update_status(self, new_payment_status_id):
        self.payment_status_id = new_payment_status_id

    def initiate_payment(self, payment_data: Dict[str, Any], payment_provider_gateway: IPaymentProviderGateway):
        payment_provider_response = payment_provider_gateway.initiate_payment(payment_data)
        self.qr_code = payment_provider_response.get("qr_data")
        self.transaction_id = payment_provider_response.get("in_store_order_id")
        return payment_provider_response


__all__ = ['Payment']

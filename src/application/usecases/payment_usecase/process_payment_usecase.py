from typing import Any, Dict

from config.settings import WEBHOOK_URL
from src.constants.payment_status import PaymentStatusEnum
from src.core.domain.entities.order import Order
from src.core.domain.entities.payment import Payment
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.core.ports.payment.i_payment_provider_gateway import IPaymentProviderGateway
from src.core.ports.payment.i_payment_repository import IPaymentRepository
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository


class ProcessPaymentUseCase:
    
    def __init__(self,
        payment_gateway: IPaymentRepository,
        payment_status_gateway: IPaymentStatusRepository,
        payment_method_gateway: IPaymentMethodRepository,
        order_gateway: IOrderRepository,
        order_status_gateway: IOrderStatusRepository,
        payment_provider_gateway: IPaymentProviderGateway
    ):
        self.payment_gateway = payment_gateway
        self.payment_status_gateway = payment_status_gateway
        self.payment_method_gateway = payment_method_gateway
        self.order_gateway = order_gateway
        self.order_status_gateway = order_status_gateway
        self.payment_provider_gateway = payment_provider_gateway
        
    @classmethod
    def build(
        cls,
        payment_gateway: IPaymentRepository,
        payment_status_gateway: IPaymentStatusRepository,
        payment_method_gateway: IPaymentMethodRepository,
        order_gateway: IOrderRepository,
        order_status_gateway: IOrderStatusRepository,
        payment_provider_gateway: IPaymentProviderGateway
    ) -> 'ProcessPaymentUseCase':
        return cls(
            payment_gateway=payment_gateway,
            payment_status_gateway=payment_status_gateway,
            payment_method_gateway=payment_method_gateway,
            order_gateway=order_gateway,
            order_status_gateway=order_status_gateway,
            payment_provider_gateway=payment_provider_gateway
        )

    def execute(self, order_id: int, method_payment: str, current_user: dict) -> Dict[str, Any]:
        order: Order = self.order_gateway.get_by_id(order_id)
        
        if not order:
            raise EntityNotFoundException("Pedido não encontrado.")
        
        validation_response = order.validate_payment(current_user)
        if validation_response:
            return validation_response

        payment_method = self.payment_method_gateway.get_by_name(method_payment)
        if not payment_method:
            raise EntityNotFoundException("Não foi possível encontrar o método de pagamento informado.")

        payment_data = order.prepare_payment_data(WEBHOOK_URL)

        payment_status = self.payment_status_gateway.get_by_name(PaymentStatusEnum.PAYMENT_PENDING.status)
        if not payment_status:
            raise ValueError(f"Status de pagamento não encontrado: {PaymentStatusEnum.PAYMENT_PENDING.status}")

        payment = Payment(
            payment_method=payment_method,
            payment_status=payment_status,
            amount=payment_data['total_amount'],
            external_reference=payment_data["external_reference"],
        )
        payment_provider_response = payment.initiate_payment(payment_data, self.payment_provider_gateway)
        
        payment = self.payment_gateway.create_payment(payment)
        order.payment = payment
        self.order_gateway.update(order)

        return {
            "payment_id": payment.id,
            "transaction_id": payment_provider_response["in_store_order_id"],
            "qr_code_link": payment_provider_response["qr_data"]
        }

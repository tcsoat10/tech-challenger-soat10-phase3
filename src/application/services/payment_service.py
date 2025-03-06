import traceback
from typing import Dict, Any
import uuid
from config.settings import WEBHOOK_URL
from src.core.domain.entities.order import Order
from src.constants.order_status import OrderStatusEnum
from src.core.exceptions.bad_request_exception import BadRequestException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.domain.entities.payment import Payment
from src.core.ports.payment.i_payment_service import IPaymentService
from src.core.ports.payment.i_payment_provider_gateway import IPaymentProviderGateway
from src.core.ports.payment.i_payment_repository import IPaymentRepository
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.constants.payment_status import PaymentStatusEnum


class PaymentService(IPaymentService):
    """
    Serviço responsável por orquestrar o processo de pagamentos e lidar com webhooks.
    """

    def __init__(
        self,
        gateway: IPaymentProviderGateway,
        repository: IPaymentRepository,
        payment_status_repository: IPaymentStatusRepository,
        payment_method_repository: IPaymentMethodRepository,
        order_repository: IOrderRepository,
        order_status_repository: IOrderStatusRepository
    ):
        self.gateway = gateway
        self.repository = repository
        self.payment_status_repository = payment_status_repository
        self.payment_method_repository = payment_method_repository
        self.order_repository = order_repository
        self.order_status_repository = order_status_repository

    def handle_webhook(self, payload: Dict[str, Any]) -> None:
        """
        Processes a webhook sent by the payment service.
        :param payload: Data sent by the payment service webhook.
        """
        try:
            payment_details = self.gateway.verify_payment(payload)
            if payment_details.get("action") == "return":
                return payment_details

            external_reference = payment_details.get("external_reference")
            status_name = payment_details.get("payment_status")

            status_mapped = self.gateway.status_map(status_name)
            if not status_mapped:
                raise BadRequestException(f"Status desconhecido recebido: {status_name}")

            # Buscando o pagamento no banco de dados
            payment = self.repository.get_payment_by_reference(external_reference)
            if not payment:
                raise BadRequestException(f"Pagamento com referência {external_reference} não encontrado.")

            # Atualizando o status do pagamento
            new_status = self.payment_status_repository.get_by_name(status_mapped.status)
            if not new_status:
                raise BadRequestException(f"Status de pagamento não encontrado: {status_name}")

            payment = self.repository.update_payment_status(payment, new_status.id)

            if new_status.name == PaymentStatusEnum.PAYMENT_COMPLETED.status and payment.order[0].order_status.status == OrderStatusEnum.ORDER_PLACED.status:
                if len(payment.order) == 0:
                    cancelled_status = self.payment_status_repository.get_by_name(PaymentStatusEnum.PAYMENT_CANCELLED.status)
                    self.repository.update_payment_status(payment, cancelled_status.id)
                    return {"message": "Pagamento cancelado, pedido não encontrado."}
                
                payment.order[0].advance_order_status(self.order_status_repository)
                self.order_repository.update(payment.order[0])

        except Exception as e:
            traceback.print_exc()
            raise BadRequestException(f"Erro ao processar webhook: {str(e)}")

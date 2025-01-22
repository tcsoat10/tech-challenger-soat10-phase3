from typing import Dict, Any
from config.settings import WEBHOOK_URL
from src.core.domain.entities.order import Order
from src.constants.order_status import OrderStatusEnum
from src.core.exceptions.bad_request_exception import BadRequestException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.domain.entities.payment import Payment
from src.core.ports.payment.i_payment_service import IPaymentService
from src.core.ports.payment.i_payment_gateway import IPaymentGateway
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
        gateway: IPaymentGateway,
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

    def process_payment(self, order_id: int, method_payment: str, current_user: dict) -> Dict[str, Any]:
        """
        Inicia o pagamento através do gateway e registra no banco de dados.
        :param order_id: ID do pedido.
        :param method_payment: Método de pagamento selecionado.
        :param current_user: Usuário autenticado.
        :return: Detalhes do pagamento.
        """
        order: Order = self.order_repository.get_by_id(order_id)
        
        if not order:
            raise EntityNotFoundException("Pedido não encontrado.")
        
        if order.id_customer != current_user["person"]["id"]:
            raise BadRequestException("Você não tem permissão para acessar este pedido.")
        
        if order.payment and order.payment.payment_status.name in [
            PaymentStatusEnum.PAYMENT_PENDING.status,
            PaymentStatusEnum.PAYMENT_COMPLETED.status
        ]:
            return {
                "payment_id": order.payment,
                "transaction_id": order.payment.transaction_id,
                "qr_code_link": order.payment.qr_code
            }

        payment_method = self.payment_method_repository.get_by_name(method_payment)
        if not payment_method:
            raise EntityNotFoundException("Não foi possível encontrar o método de pagamento informado.")

        if order.order_status.status != OrderStatusEnum.ORDER_PLACED.status:
            raise BadRequestException("Não é possível processar o pagamento neste momento.")

        payment_data = {
            "external_reference": f"order-{order.id}",
            "notification_url": f"{WEBHOOK_URL}/webhook/payment",
            "total_amount": order.total,
            "items": [
                {
                    "category": order_item.product.category.name,
                    "title": order_item.product.name,
                    "description": order_item.product.description,
                    "quantity": order_item.quantity,
                    "unit_measure": "unit",
                    "unit_price": order_item.product.price,
                    "total_amount": order_item.total
                }
                for order_item in order.order_items
            ],
            "title": f"Compra do pedido {order.id}",
            "description": f"Compra do pedido {order.id}"
        }

        payment_status = self.payment_status_repository.get_by_name(PaymentStatusEnum.PAYMENT_PENDING.status)
        if not payment_status:
            raise ValueError(f"Status de pagamento não encontrado: {PaymentStatusEnum.PAYMENT_PENDING.status}")

        gateway_response = self.gateway.initiate_payment(payment_data)

        payment = Payment(
            payment_method_id=payment_method.id,
            payment_status_id=payment_status.id,
            amount=payment_data['total_amount'],
            external_reference=gateway_response["external_reference"],
            qr_code=gateway_response.get("qr_code"),
            transaction_id=gateway_response.get("id"),
        )

        payment = self.repository.create_payment(payment)
        order.payment = payment
        self.order_repository.update(order)

        return {
            "payment_id": payment.id,
            "transaction_id": gateway_response["in_store_order_id"],
            "qr_code_link": gateway_response["qr_data"]
        }

    def handle_webhook(self, payload: Dict[str, Any]) -> None:
        """
        Processa um webhook enviado pelo serviço de pagamento.
        :param payload: Dados do webhook enviados pelo serviço de pagamento.
        """
        try:
            payment_details = self.gateway.verify_payment(payload)

            external_reference = payment_details.get("external_reference")
            status_name = payment_details.get("payment_status")

            status_reference = {
                self.gateway.status_map[PaymentStatusEnum.PAYMENT_PENDING.status]: PaymentStatusEnum.PAYMENT_PENDING.status,
                self.gateway.status_map[PaymentStatusEnum.PAYMENT_COMPLETED.status]: PaymentStatusEnum.PAYMENT_COMPLETED.status,
                self.gateway.status_map[PaymentStatusEnum.PAYMENT_CANCELLED.status]: PaymentStatusEnum.PAYMENT_CANCELLED.status,
            }

            if status_name not in status_reference:
                raise BadRequestException(f"Status desconhecido recebido: {status_name}")

            # Buscando o pagamento no banco de dados
            payment = self.repository.get_payment_by_reference(external_reference)
            if not payment:
                raise BadRequestException(f"Pagamento com referência {external_reference} não encontrado.")

            # Atualizando o status do pagamento
            new_status = self.payment_status_repository.get_by_name(status_reference[status_name])
            if not new_status:
                raise BadRequestException(f"Status de pagamento não encontrado: {status_name}")

            self.repository.update_payment_status(payment, new_status.id)

            if status_name == "closed":
                payment.order.next_step(self.order_status_repository)
                self.order_repository.update(payment.order)
        except Exception as e:
            raise BadRequestException(f"Erro ao processar webhook: {str(e)}")

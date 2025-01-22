from typing import Dict, Any
import requests
from config.settings import MERCADO_PAGO_ACCESS_TOKEN, WEBHOOK_URL
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

    #def process_payment(self, order_id: int, method_payment: str, current_user: dict) -> None:
        

    def process_payment(self,  order_id: int, method_payment: str, current_user: dict) -> Dict[str, Any]:
        """
        Inicia o pagamento através do gateway e registra no banco de dados.
        :param payment_data: Dados necessários para criar o pagamento.
        :return: Detalhes do pagamento, como QR Code ou link de checkout.
        """
        #order = self._get_order(order_id, current_user)
        order = self.order_repository.get_by_id(order_id)
        
        payment_method = self.payment_method_repository.get_by_name(method_payment)
        if not payment_method:
            raise EntityNotFoundException(message="Não foi possível encontrar o método de pagamento informado.")

        if order.order_status.status != OrderStatusEnum.ORDER_PLACED.status:
            raise BadRequestException("Não é possível processar o pagamento neste momento.")

        payment_data = {
            "external_reference": f"order-{order.id}",
            "notification_url": f"{WEBHOOK_URL}/webhook/payment",
            "total_amount": order.total,
            "items": [
                {
                    "sku_number": None, # SKU is not available
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

        '''try:
            payment_response = self.process_payment(payment_data)
            self.payments.append(payment_response) # TODO: Verificar se está correto e se é necessário

        except Exception as e:
            raise BadRequestException(f"Erro ao criar pagamento: {str(e)}")
        '''

        # Recupera o status inicial do pagamento
        payment_status = self.payment_status_repository.get_by_name(PaymentStatusEnum.PAYMENT_PENDING.status)
        if not payment_status:
            raise ValueError(f"Status de pagamento não encontrado: {PaymentStatusEnum.PAYMENT_PENDING.status}")

        # Cria o pagamento no gateway
        gateway_response = self.gateway.initiate_payment(payment_data)

        
        
        # Salva os detalhes no banco de dados

        payment = Payment(
            payment_method_id=payment_method.id,
            payment_status_id=payment_status.id,
            amount=payment_data['total_amount'],
            external_reference=gateway_response["in_store_order_id"]
        )

        payment = self.repository.create_payment(payment)
        return {
            "payment_id": payment.id,
            "transaction_id": gateway_response["in_store_order_id"],
            "qr_code_link": gateway_response["qr_data"]
        }

    def handle_webhook(self, payload: Dict[str, Any]) -> None:
        """
        Processa um webhook enviado pelo gateway e atualiza o status do pagamento.
        :param payload: Dados enviados pelo gateway.
        """
        

        headers = {
            "Authorization": f"Bearer {MERCADO_PAGO_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        status_reference = {
            'opened': PaymentStatusEnum.PAYMENT_PENDING.status,
            'closed': PaymentStatusEnum.PAYMENT_COMPLETED.status,
            'expired': PaymentStatusEnum.PAYMENT_CANCELLED.status
        }
        
        resource = payload.get('resource')
        merchan_order_id = resource.split('/')[-1]

        res = requests.get(f'https://api.mercadopago.com/merchant_orders/{merchan_order_id}', headers=headers)
        res = res.json()
        transaction_id = res.get("id")
        new_status_name = res.get("status")
        external_reference = res.get("external_reference")
        # Status do pagamento recebido no webhook
        # Recupera o status do pagamento pelo nome
        new_status = self.payment_status_repository.get_by_name(status_reference[new_status_name])
        #payment.payment_status_id = new_status.id

        # Recupera o pagamento pela referência externa
        payment = self.repository.get_payment_by_reference(external_reference)
        if not payment:
            raise ValueError(f"Pagamento com referência {transaction_id} não encontrado.")

        if new_status_name == 'closed' or new_status_name == 'expired':
            self.repository.update_payment_status(new_status.id)
        
        if new_status_name == 'closed':
            payment.order.next_step(self.order_status_repository)

from typing import Dict, Any
from src.core.domain.entities.payment import Payment
from src.core.ports.payment.i_payment_service import IPaymentService
from src.core.ports.payment.i_payment_gateway import IPaymentGateway
from src.core.ports.payment.i_payment_repository import IPaymentRepository
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository
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
        payment_method_repository: IPaymentMethodRepository
    ):
        self.gateway = gateway
        self.repository = repository
        self.payment_status_repository = payment_status_repository
        self.payment_method_repository = payment_method_repository

    def process_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inicia o pagamento através do gateway e registra no banco de dados.
        :param payment_data: Dados necessários para criar o pagamento.
        :return: Detalhes do pagamento, como QR Code ou link de checkout.
        """
        # Valida o método de pagamento
        payment_method = self.payment_method_repository.get_by_id(payment_data["payment_method_id"])
        if not payment_method:
            raise ValueError(f"Método de pagamento inválido: {payment_data['payment_method_id']}")

        # Recupera o status inicial do pagamento
        payment_status = self.payment_status_repository.get_by_name(PaymentStatusEnum.PAYMENT_PENDING.status)
        if not payment_status:
            raise ValueError(f"Status de pagamento não encontrado: {PaymentStatusEnum.PAYMENT_PENDING.status}")

        pending_status_id = payment_status.id

        # Cria o pagamento no gateway
        gateway_response = self.gateway.initiate_payment(payment_data)

        payment = Payment(
            payment_method_id=payment_data["payment_method_id"],
            payment_status_id=pending_status_id,
            amount=payment_data["amount"],
            external_reference=gateway_response["transaction_id"]
        )

        # Salva os detalhes no banco de dados
        payment = self.repository.create_payment(payment)

        return {
            "payment_id": payment.id,
            "transaction_id": gateway_response["transaction_id"],
            "qr_code_link": gateway_response["qr_code_link"]
        }

    def handle_webhook(self, payload: Dict[str, Any]) -> None:
        """
        Processa um webhook enviado pelo gateway e atualiza o status do pagamento.
        :param payload: Dados enviados pelo gateway.
        """
        transaction_id = payload.get("transaction_id")
        new_status_name = payload.get("status") # Status do pagamento recebido no webhook

        # Recupera o status do pagamento pelo nome
        new_status = self.payment_status_repository.get_by_name(new_status_name)

        # Recupera o pagamento pela referência externa
        payment = self.repository.get_payment_by_reference(transaction_id)

        payment.payment_status_id = new_status.id

        if not payment:
            raise ValueError(f"Pagamento com referência {transaction_id} não encontrado.")

        # Atualiza o status do pagamento no banco de dados
        self.repository.update_payment_status(payment_id=payment["id"], status_id=new_status.id)

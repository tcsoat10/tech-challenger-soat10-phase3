import requests
from typing import Dict, Any
from config.settings import MERCADO_PAGO_ACCESS_TOKEN, MERCADO_PAGO_USER_ID, MERCADO_PAGO_POS_ID
from src.core.ports.payment.i_payment_gateway import IPaymentGateway


class MercadoPagoGateway(IPaymentGateway):
    """
    Implementação do gateway de pagamento usando a API oficial do Mercado Pago.
    """

    def __init__(self):
        self.base_url = 'https://api.mercadopago.com'
        self.headers = {
            "Authorization": f"Bearer {MERCADO_PAGO_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

    def initiate_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria uma preferência de pagamento no Mercado Pago.
        :param payment_data: Dados para criar o pagamento.
        :return: Detalhes do pagamento, como QR Code e ID da transação.
        """
        payload = {
            "external_reference": payment_data.get("external_reference", ""),
            "notification_url": payment_data.get("notification_url", ""),
            "total_amount": payment_data.get("total_amount", 0.0),
            "items": payment_data.get("items", []),
            "title": payment_data.get("title", ""),
            "description": payment_data.get("description", "")
        }

        url = f"{self.base_url}/instore/orders/qr/seller/collectors/{MERCADO_PAGO_USER_ID}/pos/{MERCADO_PAGO_POS_ID}/qrs"
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def verify_payment(self, payment_id: str) -> Dict[str, Any]:
        """
        Verifica o status de um pagamento.
        :param payment_id: ID único do pagamento.
        :return: Detalhes do status do pagamento.
        """
        url = f"{self.base_url}/v1/payments/{payment_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

import requests
from typing import Dict, Any
from config.settings import MERCADO_PAGO_ACCESS_TOKEN, MERCADO_PAGO_USER_ID, MERCADO_PAGO_POS_ID
from src.core.ports.payment.i_payment_gateway import IPaymentGateway


class MercadoPagoGateway(IPaymentGateway):
    """
    Implementação do gateway de pagamento usando a biblioteca oficial do Mercado Pago.
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

        '''  EXAMPLE REQUEST BODY
        payment_data = {
            "external_reference": "<can add any alphanumeric identificator>",
            "notification_url":"ADD WEBHOOK URL HERE",
            "total_amount": 1000.00,
            "items": [
                {
                    "sku_number": "12312312",
                    "category": "Food",
                    "title": "<order name/tag>",
                    "description": "<order description>",
                    "quantity": 1,
                    "unit_measure": "unit",
                    "unit_price": 1000.00,
                    "total_amount": 1000.00
                }
            ],
            "title": "Compra en tienda",
            "description": "Compra en tienda" 
        }
        '''
        url = f"{self.base_url}/instore/orders/qr/seller/collectors/{MERCADO_PAGO_USER_ID}/pos/{MERCADO_PAGO_POS_ID}/qrs"
        response = requests.post(url, json=payment_data, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def verify_payment(self, payment_id: str) -> Dict[str, Any]:
        """
        Verifica o status de um pagamento.
        :param payment_id: ID único do pagamento.
        :return: Detalhes do status do pagamento.
        """
        url = f'{self.base_url}/merchant_orders/:merchanOrderId'
        response = self.sdk.payment().get(payment_id)
        if response["status"] != 200:
            raise Exception(f"Erro ao verificar pagamento: {response}")

        return response["response"]

from abc import ABC, abstractmethod
from typing import Any, Dict, List

class IPaymentService(ABC):

    @abstractmethod
    def process_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa o pagamento e retorna os detalhes relevantes, como o QR Code ou links de pagamento.
        
        :param payment_data: Dados necessários para processar o pagamento.
        :return: Um dicionário contendo os detalhes do pagamento.
        """
        pass

    @abstractmethod
    def handle_webhook(self, payload: Dict[str, Any]) -> None:
        """
        Processa eventos de webhook enviados pelo gateway de pagamento.
        
        :param payload: Dados enviados pelo gateway no evento de webhook.
        """
        pass

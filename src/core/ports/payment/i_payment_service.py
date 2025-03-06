from abc import ABC, abstractmethod
from typing import Any, Dict

class IPaymentService(ABC):

    @abstractmethod
    def handle_webhook(self, payload: Dict[str, Any]) -> None:
        """
        Processa eventos de webhook enviados pelo gateway de pagamento.
        
        :param payload: Dados enviados pelo gateway no evento de webhook.
        """
        pass

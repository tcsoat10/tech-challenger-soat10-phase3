from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from src.core.domain.entities.payment import Payment
from src.core.ports.payment.i_payment_repository import IPaymentRepository


class PaymentRepository(IPaymentRepository):
    """
    Implementação concreta do repositório de pagamentos, responsável pela interação com o banco de dados.
    """

    def __init__(self, db_session: Session):
        """
        Inicializa o repositório com uma sessão do SQLAlchemy.
        :param db_session: Sessão ativa do SQLAlchemy.
        """
        self.db_session = db_session

    def create_payment(self, payment: Payment) -> Payment:
        """
        Insere um novo pagamento na tabela `payments` e retorna o ID do pagamento criado.
        :param payment: Instância do pagamento a ser criado.
        :return: ID do pagamento criado.
        """
        self.db_session.add(payment)
        self.db_session.commit()
        self.db_session.refresh(payment)
        return payment
        

    def update_payment_status(self, payment: Payment, status_id: int) -> Payment:
        """
        Atualiza o status de um pagamento na tabela `payments`.
        :param payment: Instância do pagamento a ser atualizado.
        :param status_id: Novo ID do status do pagamento.
        :return: Instância do pagamento atualizado.
        """
        payment.payment_status_id = status_id
        self.db_session.merge(payment)
        self.db_session.commit()
        return payment

    def get_payment_by_id(self, payment_id: int) -> Payment:
        """
        Recupera os detalhes de um pagamento pelo ID.
        :param payment_id: ID do pagamento.
        :return: Instância do pagamento.
        """
        return self.db_session.query(Payment).filter(Payment.id == payment_id).first()
        

    def get_payment_by_reference(self, external_reference: str) -> Payment:
        """
        Recupera os detalhes de um pagamento pela referência externa.
        :param external_reference: Referência externa do pagamento.
        :return: Instância do pagamento.
        """
        return self.db_session.query(Payment).filter(Payment.external_reference == external_reference).first()
        
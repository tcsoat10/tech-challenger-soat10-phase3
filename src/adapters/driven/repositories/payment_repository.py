
from sqlalchemy.orm import Session
from src.adapters.driven.repositories.models.payment_method_model import PaymentMethodModel
from src.adapters.driven.repositories.models.payment_status_model import PaymentStatusModel
from src.adapters.driven.repositories.models.payment_model import PaymentModel
from src.core.shared.identity_map import IdentityMap
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
        self.identity_map: IdentityMap = IdentityMap.get_instance()

    def create_payment(self, payment: Payment) -> Payment:
        """
        Insere um novo pagamento na tabela `payments` e retorna o ID do pagamento criado.
        :param payment: Instância do pagamento a ser criado.
        :return: ID do pagamento criado.
        """
        if payment.id is not None:
            existing_payment = self.identity_map.get(Payment, payment.id)
            if existing_payment is not None:
                self.identity_map.remove(payment)
        
        payment_model = PaymentModel.from_entity(payment)
        self.db_session.add(payment_model)
        self.db_session.commit()
        self.db_session.refresh(payment_model)
        return payment_model.to_entity()
        

    def update_payment_status(self, payment: Payment, status_id: int) -> Payment:
        """
        Atualiza o status de um pagamento na tabela `payments`.
        :param payment: Instância do pagamento a ser atualizado.
        :param status_id: Novo ID do status do pagamento.
        :return: Instância do pagamento atualizado.
        """
        if payment.id is not None:
            existing_payment = self.identity_map.get(Payment, payment.id)
            if existing_payment is not None:
                self.identity_map.remove(payment)

        payment_model = PaymentModel.from_entity(payment)
        payment_model.payment_method = PaymentMethodModel.from_entity(payment.payment_method)
        
        payment_model.payment_status_id = status_id
        payment_model.payment_status = self.db_session.query(PaymentStatusModel).filter(PaymentStatusModel.id == status_id).first()

        self.db_session.merge(payment_model)
        self.db_session.commit()
        return payment_model.to_entity()

    def get_payment_by_id(self, payment_id: int) -> Payment:
        """
        Recupera os detalhes de um pagamento pelo ID.
        :param payment_id: ID do pagamento.
        :return: Instância do pagamento.
        """
        payment_model = self.db_session.query(PaymentModel).filter(PaymentModel.id == payment_id).first()
        if payment_model is None:
            return None
        return payment_model.to_entity()
        

    def get_payment_by_reference(self, external_reference: str) -> Payment:
        """
        Recupera os detalhes de um pagamento pela referência externa.
        :param external_reference: Referência externa do pagamento.
        :return: Instância do pagamento.
        """
        payment_model = self.db_session.query(PaymentModel).filter(PaymentModel.external_reference == external_reference).first()
        if payment_model is None:
            return None
        return payment_model.to_entity()
        
import pytest
from sqlalchemy.exc import IntegrityError

from src.constants.payment_status import PaymentStatusEnum
from src.core.ports.payment.i_payment_repository import IPaymentRepository
from src.adapters.driven.repositories.payment_repository import PaymentRepository
from src.core.domain.entities.payment import Payment
from tests.factories.payment_factory import PaymentFactory
from tests.factories.payment_method_factory import PaymentMethodFactory
from tests.factories.payment_status_factory import PaymentStatusFactory


class TestPaymentRepository:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.payment_gateway: IPaymentRepository = PaymentRepository(db_session)
        self.db_session = db_session
        self.clean_database()

    def clean_database(self):
        self.db_session.query(Payment).delete()
        self.db_session.commit()

    def test_create_payment_success(self):
        payment_method = PaymentMethodFactory()
        payment_status = PaymentStatusFactory()

        payment = Payment(
            payment_method_id=payment_method.id,
            payment_status_id=payment_status.id,
            amount=100.0,
            external_reference="123456",
            qr_code="QrCode",
            transaction_id="1234"
        )

        created_payment = self.payment_gateway.create_payment(payment)

        assert created_payment.id is not None
        assert created_payment.payment_method_id == payment_method.id
        assert created_payment.payment_status_id == payment_status.id
    
    def test_create_payment_invalid_data_raises_error(self):
        payment_method = PaymentMethodFactory()
        payment_status = PaymentStatusFactory()
        payment = Payment(
            payment_method_id=payment_method.id,
            payment_status_id=payment_status.id,
            amount=100.0,
            external_reference=None,  # Inválido
            qr_code="QrCode",
            transaction_id="1234"
        )
        with pytest.raises(IntegrityError):
            self.payment_gateway.create_payment(payment)

    def test_get_payment_by_id_success(self):
        payment = PaymentFactory()

        data = self.payment_gateway.get_payment_by_id(payment.id)

        assert data is not None
        assert data.id == payment.id
        assert data.payment_method_id == payment.payment_method_id
        assert data.payment_status_id == payment.payment_status_id

    def test_get_payment_by_id_returns_none_unregistered_id(self):
        payment = PaymentFactory()

        data = self.payment_gateway.get_payment_by_id(payment.id + 1)

        assert data is None
        
    def test_payment_status_methods(self):
        pending_status = PaymentStatusFactory(name=PaymentStatusEnum.PAYMENT_PENDING.status)
        completed_status = PaymentStatusFactory(name=PaymentStatusEnum.PAYMENT_COMPLETED.status)
        cancelled_status = PaymentStatusFactory(name=PaymentStatusEnum.PAYMENT_CANCELLED.status)
        
        payment_pending = PaymentFactory(payment_status=pending_status)
        payment_completed = PaymentFactory(payment_status=completed_status)
        payment_cancelled = PaymentFactory(payment_status=cancelled_status)
        
        assert payment_pending.is_pending() is True
        assert payment_completed.is_completed() is True
        assert payment_cancelled.is_cancelled() is True
    
    def test_update_payments_payment_status_success(self):
        payment = PaymentFactory()
        payment_status = PaymentStatusFactory()

        updated_payment = self.payment_gateway.update_payment_status(payment, payment_status.id)

        assert updated_payment.id == payment.id
        assert updated_payment.payment_status_id == payment_status.id
        
    def test_update_payment_status_same_status(self):
        payment_status = PaymentStatusFactory()
        payment = PaymentFactory(payment_status_id=payment_status.id)
        
        # Atualiza com o mesmo status
        updated_payment = self.payment_gateway.update_payment_status(payment, payment_status.id)
        
        assert updated_payment.payment_status_id == payment_status.id
    
    def test_update_payments_payment_status_unregistered_id(self):
        payment = PaymentFactory()
        payment_status = PaymentStatusFactory()

        with pytest.raises(IntegrityError):
            self.payment_gateway.update_payment_status(payment, payment_status.id + 1)
        
    def test_get_payment_by_reference_success(self):
        payment = PaymentFactory()

        data = self.payment_gateway.get_payment_by_reference(payment.external_reference)

        assert data is not None
        assert data.id == payment.id
        assert data.external_reference == payment.external_reference
        
    def test_get_payment_by_reference_returns_none_unregistered_reference(self):
        payment = PaymentFactory()

        data = self.payment_gateway.get_payment_by_reference(payment.external_reference + "1")

        assert data is None

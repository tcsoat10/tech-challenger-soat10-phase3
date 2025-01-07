
import pytest
from sqlalchemy.exc import IntegrityError

from src.core.domain.entities.payment_status import PaymentStatus
from src.adapters.driven.repositories.payment_status_repository import PaymentStatusRepository
from tests.factories.payment_status_factory import PaymentStatusFactory


class TestPaymentStatusRepository:

    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.repository = PaymentStatusRepository(db_session)
        self.db_session = db_session
        self.clean_database()

    def clean_database(self):
        self.db_session.query(PaymentStatus).delete()
        self.db_session.commit()

    def test_create_payment_status_success(self):
        payment_status = PaymentStatus(name="Paid", description="Payment status paid")
        created_payment_status = self.repository.create(payment_status)

        assert created_payment_status.id is not None
        assert created_payment_status.name == "Paid"
        assert created_payment_status.description == "Payment status paid"

        db_payment_status = self.db_session.query(PaymentStatus).filter_by(name="Paid").first()
        assert db_payment_status is not None
        assert db_payment_status.name == "Paid"
        assert db_payment_status.description == "Payment status paid"

    def test_try_create_payment_status_duplicated_with_repository_and_raise_error(self):
        PaymentStatusFactory(name="Paid", description="Payment status paid")

        new = PaymentStatus(name="Paid", description="Payment status paid")
        with pytest.raises(IntegrityError):
            self.repository.create(new)

    def test_get_payment_status_by_name_success(self):
        PaymentStatusFactory(name="Paid", description="Payment status paid")

        payment_status_from_db = self.repository.get_by_name("Paid")
        
        assert payment_status_from_db is not None
        assert payment_status_from_db.name == "Paid"
        assert payment_status_from_db.description == "Payment status paid"

    def test_get_payment_status_by_id_success(self):
        payment_status = PaymentStatusFactory(name="Paid", description="Payment status paid")

        payment_status_from_db = self.repository.get_by_id(payment_status.id)
        
        assert payment_status_from_db is not None
        assert payment_status_from_db.name == "Paid"
        assert payment_status_from_db.description == "Payment status paid"

    def test_get_all_payment_statuses_success(self):
        PaymentStatusFactory(name="Paid", description="Payment status paid")
        PaymentStatusFactory(name="Pending", description="Payment status pending")

        payment_statuses_from_db = self.repository.get_all()
        
        assert len(payment_statuses_from_db) == 2
        assert payment_statuses_from_db[0].name == "Paid"
        assert payment_statuses_from_db[0].description == "Payment status paid"
        assert payment_statuses_from_db[1].name == "Pending"
        assert payment_statuses_from_db[1].description == "Payment status pending"

    def test_get_all_payment_statuses_empty(self):
        payment_statuses_from_db = self.repository.get_all()
        
        assert len(payment_statuses_from_db) == 0

    def test_update_payment_status_success(self):
        payment_status = PaymentStatusFactory(name="Paid", description="Payment status paid")

        payment_status.name = "Pending"
        payment_status.description = "Payment status pending"
        updated_payment_status = self.repository.update(payment_status)

        assert updated_payment_status.id is not None
        assert updated_payment_status.name == "Pending"
        assert updated_payment_status.description == "Payment status pending"
    
    def test_delete_payment_status(self):
        payment_status = PaymentStatusFactory(name="Paid", description="Payment status paid")
        self.repository.delete(payment_status)

        assert len(self.repository.get_all()) == 0

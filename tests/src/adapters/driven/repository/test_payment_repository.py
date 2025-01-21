# import pytest

# from src.adapters.driven.repositories.payment_repository import PaymentRepository
# from src.core.domain.entities.payment import Payment
# from tests.factories.payment_status_factory import PaymentStatusFactory
# from tests.factories.payment_method_factory import PaymentMethodFactory
# from tests.factories.payment_factory import PaymentFactory


# class TestPaymentRepository:
#     @pytest.fixture(autouse=True)
#     def setup(self, db_session):
#         self.repository = PaymentRepository(db_session)
#         self.db_session = db_session
#         self.clean_database()

#     def clean_database(self):
#         self.db_session.query(Payment).delete()
#         self.db_session.commit()

#     def test_create_payment_success(self):
#         payment_method = PaymentMethodFactory()
#         payment_status = PaymentStatusFactory()

#         payment = Payment(payment_method_id=payment_method.id, payment_status_id=payment_status.id)

#         created_payment = self.repository.create(payment)

#         assert created_payment.id is not None
#         assert created_payment.payment_method_id == payment_method.id
#         assert created_payment.payment_status_id == payment_status.id
    
#     def test_get_payment_by_id_success(self):
#         payment = PaymentFactory()

#         data = self.repository.get_by_id(payment.id)

#         assert data is not None
#         assert data.id == payment.id
#         assert data.payment_method_id == payment.payment_method_id
#         assert data.payment_status_id == payment.payment_status_id
    
#     def test_get_payment_by_id_returns_none_unregistered_id(self):
#         payment = PaymentFactory()

#         data = self.repository.get_by_id(payment.id + 1)

#         assert data is None

#     def test_get_payments_by_payment_method_id(self):
#         payment_method = PaymentMethodFactory()

#         payment1 = PaymentFactory(payment_method=payment_method)
#         payment2 = PaymentFactory(payment_method=payment_method)
#         payment3 = PaymentFactory()

#         data = self.repository.get_by_method_id(payment_method.id)

#         assert data is not None
#         assert len(data) == 2
#         assert data == [payment1, payment2]
    
#     def test_get_payments_by_payment_status_id(self):
#         payment_status = PaymentStatusFactory()

#         payment1 = PaymentFactory(payment_status=payment_status)
#         payment2 = PaymentFactory(payment_status=payment_status)
#         payment3 = PaymentFactory()

#         data = self.repository.get_by_status_id(payment_status.id)

#         assert data is not None
#         assert len(data) == 2
#         assert data == [payment1, payment2]
    
#     def test_get_payment_by_method_id_returns_none_unregistered_id(self):
#         payment = PaymentFactory()

#         data = self.repository.get_by_method_id(payment.payment_method_id + 1)

#         assert data == []

#     def test_get_payment_by_status_id_returns_none_unregistered_id(self):
#         payment = PaymentFactory()

#         data = self.repository.get_by_status_id(payment.payment_status_id + 1)

#         assert data == []
    
#     def test_get_all_payments_success(self):
#         payment1 = PaymentFactory()
#         payment2 = PaymentFactory()

#         data = self.repository.get_all()

#         assert len(data) == 2
#         assert data == [payment1, payment2]
    
#     def test_get_all_payments_empty_db(self):
#         data = self.repository.get_all()

#         assert data == []

#     def test_update_payment_success(self):
#         payment = PaymentFactory()

#         method = PaymentMethodFactory()
#         status = PaymentStatusFactory()

#         payment.payment_method_id = method.id
#         payment.payment_status_id = status.id

#         data = self.repository.update(payment)

#         assert data.id == payment.id
#         assert data.payment_method_id == method.id
#         assert data.payment_status_id == status.id

#     def test_delete_payment(self):
#         payment = PaymentFactory()

#         self.repository.delete(payment.id)

#         data = self.repository.get_all()

#         assert len(data) == 0
#         assert data == []

#     def test_delete_payment_unregistered_id(self):
#         payment = PaymentFactory()

#         self.repository.delete(payment.id + 1)

#         data = self.repository.get_all()

#         assert len(data) == 1
#         assert data == [payment]
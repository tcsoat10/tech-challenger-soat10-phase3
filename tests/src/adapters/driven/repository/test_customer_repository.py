import pytest

from src.adapters.driven.repositories.customer_repository import CustomerRepository
from src.core.domain.entities.customer import Customer
from tests.factories.person_factory import PersonFactory
from tests.factories.customer_factory import CustomerFactory


class TestCustomerRepository:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.repository = CustomerRepository(db_session)
        self.db_session = db_session
        self.clean_database()
    
    def clean_database(self):
        self.db_session.query(Customer).delete()
        self.db_session.commit()

    def test_create_customer_success(self):
        person = PersonFactory()
        customer = Customer(person_id=person.id)

        created_customer = self.repository.create(customer)

        assert created_customer.id is not None
        assert created_customer.person_id == person.id
    
    def test_get_customer_by_id_success(self):
        customer = CustomerFactory()

        customer_response = self.repository.get_by_id(customer.id)

        assert customer_response is not None
        assert customer_response.id == customer.id
        assert customer_response.person_id == customer.person_id
    
    def test_get_customer_by_id_returns_none_for_unregistered_id(self):
        customer = CustomerFactory()

        customer_response = self.repository.get_by_id(customer.id + 1)

        assert customer_response is None

    def test_get_by_cpf_success(self):
        customer = CustomerFactory()

        customer_response = self.repository.get_by_cpf(customer.person.cpf)

        assert customer_response is not None
        assert customer_response.id == customer.id
        assert customer_response.person_id == customer.person_id

    def test_get_by_cpf_returns_none_for_unregistered_cpf(self):
        customer = CustomerFactory()

        customer_response = self.repository.get_by_cpf(customer.person.cpf + "1")

        assert customer_response is None

    def test_get_customer_by_person_id_success(self):
        customer = CustomerFactory()

        customer_response = self.repository.get_by_person_id(customer.person_id)

        assert customer_response is not None
        assert customer_response.id == customer.id
        assert customer_response.person_id == customer.person_id
    
    def test_get_customer_by_person_id_returns_none_for_unregistered_id(self):
        customer = CustomerFactory()

        customer_response = self.repository.get_by_person_id(customer.person_id + 1)

        assert customer_response is None

    def test_get_all_customers_success(self):
        customer1 = CustomerFactory()
        customer2 = CustomerFactory()

        customers = self.repository.get_all()

        assert len(customers) == 2
        assert customers == [customer1, customer2]

    def test_get_all_customers_empty_db(self):
        customers = self.repository.get_all()

        assert len(customers) == 0
        assert customers == []

    def test_update_customer(self):
        customer = CustomerFactory()
        person = PersonFactory()

        customer.person_id = person.id

        data = self.repository.update(customer)

        assert data.id == customer.id
        assert data.person_id == person.id

    def test_delete_customer_success(self):
        customer = CustomerFactory()

        self.repository.delete(customer.id)

        customers = self.repository.get_all()

        assert len(customers) == 0
        assert customers == []

    def test_delete_customer_unregistered_id(self):
        customer = CustomerFactory()

        self.repository.delete(customer.id + 1)

        customers = self.repository.get_all()

        assert len(customers) == 1
        assert customers == [customer]

    
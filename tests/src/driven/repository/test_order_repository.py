import pytest
from sqlalchemy.exc import IntegrityError

from src.core.domain.entities.customer import Customer
from src.core.domain.entities.person import Person
from src.adapters.driven.repositories.order_repository import OrderRepository
from src.core.domain.entities.order import Order
from tests.factories.customer_factory import CustomerFactory
from tests.factories.employee_factory import EmployeeFactory
from tests.factories.order_factory import OrderFactory
from tests.factories.order_status_factory import OrderStatusFactory
from tests.factories.person_factory import PersonFactory


class TestOrderRepository:

    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.repository = OrderRepository(db_session)
        self.db_session = db_session
        self.clean_database()

    def clean_database(self):
        self.db_session.query(Order).delete()
        self.db_session.commit()

    def test_create_order_success(self):
        customer = CustomerFactory()
        order_status = OrderStatusFactory()
        employee = EmployeeFactory()
        order = Order(customer=customer, order_status=order_status, employee=employee)
        created_order = self.repository.create(order)

        assert created_order.id is not None
        assert created_order.id_customer == customer.id
        assert created_order.id_order_status == order_status.id
        assert created_order.id_employee == employee.id

    # def test_try_create_order_duplicated_with_repository_and_raise_error(self):
    #     customer = CustomerFactory()
    #     order_status = OrderStatusFactory()
    #     OrderFactory(customer=customer, order_status=order_status)
    #     order = Order(customer=customer, order_status=order_status)
    #     with pytest.raises(IntegrityError):
    #         self.repository.create(order)

    def test_get_order_by_customer_id_success(self):
        customer = CustomerFactory()
        order_status = OrderStatusFactory()
        employee = EmployeeFactory()
        order = Order(customer=customer, order_status=order_status, employee=employee)
        self.repository.create(order)

        order_from_db = self.repository.get_by_customer_id(order.id_customer)
        assert order_from_db is not None
    
    def test_get_order_by_employee_id_success(self):
        customer = CustomerFactory()
        order_status = OrderStatusFactory()
        employee = EmployeeFactory()
        order = Order(customer=customer, order_status=order_status, employee=employee)
        self.repository.create(order)

        order_from_db = self.repository.get_by_customer_id(order.id_customer)
        assert order_from_db is not None

    def test_get_by_id_success(self):
        person_customer = PersonFactory(cpf="12345678901", name="JOÃO", email="joao@gmail.com")
        person_employee = PersonFactory(cpf="12345678902", name="PAULO", email="paulo@outlook.com")
        customer = CustomerFactory(person=person_customer)
        order_status = OrderStatusFactory()
        employee = EmployeeFactory(person=person_employee)
        order = Order(id_customer=customer.id, id_order_status=order_status.id, id_employee=employee.id, customer=customer, order_status=order_status, employee=employee)
        self.repository.create(order)
        order_from_db = self.repository.get_by_id(order.id)

        assert order_from_db is not None
        assert order_from_db.customer.person.cpf == "12345678901"
        assert order_from_db.customer.person.name == "JOÃO"
        assert order_from_db.customer.person.email == "joao@gmail.com"
        assert order_from_db.employee.person.cpf == "12345678902"
        assert order_from_db.employee.person.name == "PAULO"
        assert order_from_db.employee.person.email == "paulo@outlook.com"

    def test_get_all_success(self):
        person1 = PersonFactory(cpf="12345678901", name="JOÃO", email="joao@gmail.com")
        customer = CustomerFactory(person=person1)
        order_status = OrderStatusFactory()
        employee = EmployeeFactory()
        OrderFactory(customer=customer, order_status=order_status, employee=employee)
        
        person2 = PersonFactory(cpf="12345678902", name="PAULO", email="paulo@outlook.com")
        customer = CustomerFactory(person=person2)
        order_status = OrderStatusFactory()
        employee = EmployeeFactory()
        OrderFactory(customer=customer, order_status=order_status, employee=employee)

        orderes_from_db = self.repository.get_all()

        assert len(orderes_from_db) == 2
        assert orderes_from_db[0].customer.person.cpf == "12345678901"
        assert orderes_from_db[0].customer.person.name == "JOÃO"
        assert orderes_from_db[0].customer.person.email == "joao@gmail.com"
        assert orderes_from_db[1].customer.person.cpf == "12345678902"
        assert orderes_from_db[1].customer.person.name == "PAULO"
        assert orderes_from_db[1].customer.person.email == "paulo@outlook.com"

    def test_update_order_success(self):
        person1 = PersonFactory(cpf="12345678901", name="JOÃO", email="joao@gmail.com")
        customer1 = CustomerFactory(person=person1)
        #person2 = PersonFactory(cpf="12345678902", name="PAULO", email="paulo@outlook.com")
        #customer2 = CustomerFactory(person=person2)
        order_status = OrderStatusFactory()
        employee = EmployeeFactory()
        order = OrderFactory(customer=customer1, order_status=order_status, employee=employee)

        #Dá para atualizar direto no campo passando o caminho correto.
        order.customer.person.cpf = "12345678902"
        order.customer.person.name = "PAULO"
        order.customer.person.email = "paulo@outlook.com"
        # order.id_customer = customer2.id
        updated_order = self.repository.update(order)

        assert updated_order.id is not None
        assert updated_order.customer.person.cpf == "12345678902"
        assert updated_order.customer.person.name == "PAULO"
        assert updated_order.customer.person.email == "paulo@outlook.com"

    def test_delete_order_success(self):
        person = PersonFactory(cpf="12345678901", name="JOÃO", email="joao@gmail.com")
        customer = CustomerFactory(person=person)
        order_status = OrderStatusFactory()
        employee = EmployeeFactory()
        order = OrderFactory(customer=customer, order_status=order_status, employee=employee)

        self.repository.delete(order)

        db_order = self.db_session.query(Order).join(Customer).join(Person).filter_by(name="JOÃO").first()
        assert db_order is None
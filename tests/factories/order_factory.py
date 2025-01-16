import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker

from src.core.domain.entities.order import Order
from tests.factories.customer_factory import CustomerFactory
from tests.factories.employee_factory import EmployeeFactory
from tests.factories.order_item_factory import OrderItemFactory
from tests.factories.order_status_factory import OrderStatusFactory

fake = Faker()

class OrderFactory(SQLAlchemyModelFactory):
    
    class Meta:
        model = Order
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n + 1)
    order_status = factory.SubFactory(OrderStatusFactory)
    id_order_status = factory.SelfAttribute("order_status.id")

    customer = factory.SubFactory(CustomerFactory)
    id_customer = factory.SelfAttribute("customer.id")

    employee = factory.SubFactory(EmployeeFactory)
    id_employee = factory.SelfAttribute("employee.id")
    
    order_items = factory.RelatedFactoryList(
        OrderItemFactory,
        factory_related_name="order",
        size=0
    )

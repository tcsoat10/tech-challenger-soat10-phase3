from faker import Faker
from factory.alchemy import SQLAlchemyModelFactory
import factory

from src.core.domain.entities.order_payment import OrderPayment
from tests.factories.order_factory import OrderFactory
from tests.factories.payment_factory import PaymentFactory


fake = Faker()


class OrderPaymentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = OrderPayment
        sqlalchemy_session_persistence = 'commit'

    id = factory.Sequence(lambda n: n + 1)
    order = factory.SubFactory(OrderFactory)
    order_id = factory.SelfAttribute('order.id')
    payment = factory.SubFactory(PaymentFactory)
    payment_id = factory.SelfAttribute('payment.id')
from faker import Faker
from factory.alchemy import SQLAlchemyModelFactory
import factory

from src.core.domain.entities.payment import Payment
from tests.factories.payment_method_factory import PaymentMethodFactory
from tests.factories.payment_status_factory import PaymentStatusFactory


fake = Faker()


class PaymentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Payment
        sqlalchemy_session_persistence = 'commit'
    
    id = factory.Sequence(lambda n: n + 1)
    payment_method = factory.SubFactory(PaymentMethodFactory)
    payment_method_id = factory.SelfAttribute('payment_method.id')
    payment_status = factory.SubFactory(PaymentStatusFactory)
    payment_status_id = factory.SelfAttribute('payment_status.id')

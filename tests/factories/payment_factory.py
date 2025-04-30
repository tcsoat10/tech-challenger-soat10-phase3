from faker import Faker
from factory.alchemy import SQLAlchemyModelFactory
import factory

from src.adapters.driven.repositories.models.payment_model import PaymentModel
from tests.factories.payment_method_factory import PaymentMethodFactory
from tests.factories.payment_status_factory import PaymentStatusFactory


fake = Faker()


class PaymentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = PaymentModel
        sqlalchemy_session_persistence = 'commit'
    

    payment_method = factory.SubFactory(PaymentMethodFactory)
    payment_method_id = factory.SelfAttribute('payment_method.id')
    payment_status = factory.SubFactory(PaymentStatusFactory)
    payment_status_id = factory.SelfAttribute('payment_status.id')
    amount = factory.Faker('pyfloat', positive=True, min_value=1, max_value=1000)
    external_reference = factory.Faker('uuid4')
    qr_code = factory.LazyAttribute(lambda _: fake.url())
    transaction_id = factory.Faker('uuid4')

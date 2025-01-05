import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker

from src.core.domain.entities.payment_method import PaymentMethod

fake = Faker()

class PaymentMethodFactory(SQLAlchemyModelFactory):

    class Meta:
        model = PaymentMethod
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n + 1)
    name = factory.LazyAttribute(lambda _: fake.word())
    description = factory.LazyAttribute(lambda _: fake.sentence(nb_words=10))

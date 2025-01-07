import factory
from faker import Faker
from factory.alchemy import SQLAlchemyModelFactory

from src.core.domain.entities.payment_status import PaymentStatus

fake = Faker()

class PaymentStatusFactory(SQLAlchemyModelFactory):

    class Meta:
        model = PaymentStatus
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n + 1)
    name = factory.LazyAttribute(lambda _: fake.unique.word().capitalize())
    description = factory.LazyAttribute(lambda _: fake.sentence(nb_words=10))

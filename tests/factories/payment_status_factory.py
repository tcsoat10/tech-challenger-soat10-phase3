import factory
from faker import Faker
from factory.alchemy import SQLAlchemyModelFactory

from src.adapters.driven.repositories.models.payment_status_model import PaymentStatusModel

fake = Faker()

class PaymentStatusFactory(SQLAlchemyModelFactory):

    class Meta:
        model = PaymentStatusModel
        sqlalchemy_session_persistence = "commit"

    name = factory.LazyAttribute(lambda _: fake.unique.word().capitalize())
    description = factory.LazyAttribute(lambda _: fake.sentence(nb_words=10))

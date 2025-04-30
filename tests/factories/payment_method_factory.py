import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker

from src.adapters.driven.repositories.models.payment_method_model import PaymentMethodModel

fake = Faker()

class PaymentMethodFactory(SQLAlchemyModelFactory):

    class Meta:
        model = PaymentMethodModel
        sqlalchemy_session_persistence = "commit"

    name = factory.LazyAttribute(lambda _: fake.word())
    description = factory.LazyAttribute(lambda _: fake.sentence(nb_words=10))

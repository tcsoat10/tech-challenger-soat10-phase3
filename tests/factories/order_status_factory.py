import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker

from src.core.domain.entities.order_status import OrderStatus

fake = Faker()

class OrderStatusFactory(SQLAlchemyModelFactory):
    
    class Meta:
        model = OrderStatus
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n + 1)
    status = factory.LazyAttribute(lambda _: fake.sentence(nb_words=2))
    status_description = factory.LazyAttribute(lambda _: fake.sentence(nb_words=10))
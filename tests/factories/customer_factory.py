from faker import Faker
from factory.alchemy import SQLAlchemyModelFactory
import factory

from src.adapters.driven.repositories.models.customer_model import CustomerModel
from tests.factories.person_factory import PersonFactory


fake = Faker()


class CustomerFactory(SQLAlchemyModelFactory):
    class Meta:
        model = CustomerModel
        sqlalchemy_session_persistence = 'commit'

    id = factory.Sequence(lambda n: n + 1)
    person = factory.SubFactory(PersonFactory)
    person_id = factory.SelfAttribute('person.id')
    
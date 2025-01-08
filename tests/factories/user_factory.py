from faker import Faker
from factory.alchemy import SQLAlchemyModelFactory
import factory

from src.core.domain.entities.user import User


fake = Faker()


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = 'commit'
    
    id = factory.Sequence(lambda n: n + 1)
    name = factory.LazyAttribute(lambda _: fake.unique.word())
    password = factory.LazyAttribute(lambda _: fake.unique.word())

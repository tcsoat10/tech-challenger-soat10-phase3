from faker import Faker
from factory.alchemy import SQLAlchemyModelFactory
import factory

from src.core.domain.entities.role import Role


fake = Faker()


class RoleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Role
        sqlalchemy_session_persistence = 'commit'

    id = factory.Sequence(lambda n: n + 1)
    name = factory.LazyAttribute(lambda _: fake.unique.word().capitalize())
    description = factory.LazyAttribute(lambda _: fake.sentence(nb_words=10))
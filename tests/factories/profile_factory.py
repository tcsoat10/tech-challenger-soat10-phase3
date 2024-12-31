import factory
from faker import Faker
from factory.alchemy import SQLAlchemyModelFactory

from src.core.domain.entities.profile import Profile

fake = Faker()

class ProfileFactory(SQLAlchemyModelFactory):

    class Meta:
        model = Profile
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n + 1)
    name = factory.LazyAttribute(lambda _: fake.unique.word().capitalize())
    description = factory.LazyAttribute(lambda _: fake.sentence(nb_words=10))

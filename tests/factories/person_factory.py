import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker

from src.core.domain.entities.person import Person

fake = Faker()

class PersonFactory(SQLAlchemyModelFactory):
    
    class Meta:
        model = Person
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n + 1)
    cpf = factory.LazyAttribute(lambda _: fake.ssn())
    name = factory.LazyAttribute(lambda _: fake.unique.word().capitalize())
    email = factory.LazyAttribute(lambda _: fake.sentence(nb_words=10))
    birth_date = factory.LazyAttribute(lambda _: fake.date_of_birth(minimum_age=5, maximum_age=100))
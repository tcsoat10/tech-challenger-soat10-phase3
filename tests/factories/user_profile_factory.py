
import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker
from src.core.domain.entities.user_profile import UserProfile
from tests.factories.profile_factory import ProfileFactory
from tests.factories.user_factory import UserFactory

fake = Faker()

class UserProfileFactory(SQLAlchemyModelFactory):
    class Meta:
        model = UserProfile
        sqlalchemy_session_persistence = 'commit'

    id = factory.Sequence(lambda n: n + 1)
    user = factory.SubFactory(UserFactory)
    user_id = factory.SelfAttribute('user.id')
    profile = factory.SubFactory(ProfileFactory)
    profile_id = factory.SelfAttribute('profile.id')

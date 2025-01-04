import factory
from faker import Faker
from factory.alchemy import SQLAlchemyModelFactory

from src.core.domain.entities.profile_permission import ProfilePermission
from tests.factories.profile_factory import ProfileFactory
from tests.factories.permission_factory import PermissionFactory


fake = Faker()

class ProfilePermissionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = ProfilePermission
        sqlalchemy_session_persistence = 'commit'
    
    id = factory.Sequence(lambda n: n + 1)
    profile = factory.SubFactory(ProfileFactory)
    profile_id = factory.SelfAttribute('profile.id')
    permission = factory.SubFactory(PermissionFactory)
    permission_id = factory.SelfAttribute('permission.id')
    

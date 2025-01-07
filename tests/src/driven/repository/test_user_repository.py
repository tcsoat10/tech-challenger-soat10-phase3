import pytest

from src.adapters.driven.repositories.user_repository import UserRepository
from src.core.domain.entities.user import User


class TestUserRepository:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.repository = UserRepository(db_session)
        self.db_session = db_session
        self.clean_database()

    def clean_database(self):
        self.db_session.query(User).delete()
        self.db_session.commit()

    def test_create_user_success(self):
        new_user = User(name='Test User', password='test_pass')
        created_user = self.repository.create(new_user)

        assert created_user.id is not None
        assert created_user.name == new_user.name
        assert self.repository.verify_password('test_pass', created_user) == True
    

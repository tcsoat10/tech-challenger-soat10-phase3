from src.core.ports.user.i_user_repository import IUserRepository
from src.core.domain.entities.user import User

from sqlalchemy.orm import Session
import bcrypt


class UserRepository(IUserRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, user: User) -> User:
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user
    
    def verify_password(self, password: str, user: User):
        enc_pw = password.encode('utf-8')
        return bcrypt.checkpw(enc_pw, bytes(user.password_hash, 'utf-8'))
    
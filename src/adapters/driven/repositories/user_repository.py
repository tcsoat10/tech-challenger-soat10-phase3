from src.core.ports.user.i_user_repository import IUserRepository
from src.core.domain.entities.user import User

from sqlalchemy.orm import Session
import bcrypt
from typing import List


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
    
    def get_by_name(self, name: str) -> User:
        return self.db_session.query(User).filter(User.name == name).first()
    
    def get_by_id(self, user_id: int) -> User:
        return self.db_session.query(User).filter(User.id == user_id).first()

    def get_all(self) -> List[User]:
        return self.db_session.query(User).all()
    
    def update(self, user: User) -> User:
        self.db_session.merge(user)
        self.db_session.commit()
        return user
    
    def delete(self, user_id: int) -> None:
        user = self.get_by_id(user_id)
        if user:
            self.db_session.delete(user)
            self.db_session.commit()
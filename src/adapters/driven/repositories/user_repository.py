from src.core.ports.user.i_user_repository import IUserRepository
from src.core.domain.entities.user import User

from sqlalchemy.orm import Session
from typing import List


class UserRepository(IUserRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, user: User) -> User:
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user
    
    def get_by_name(self, name: str) -> User:
        return self.db_session.query(User).filter(User.name == name).first()
    
    def get_by_id(self, user_id: int) -> User:
        return self.db_session.query(User).filter(User.id == user_id).first()

    def get_all(self, include_deleted: bool = False) -> List[User]:
        query =  self.db_session.query(User)
        if not include_deleted:
            query = query.filter(User.inactivated_at.is_(None))
        return query.all()
    
    def update(self, user: User) -> User:
        self.db_session.merge(user)
        self.db_session.commit()
        return user
    
    def delete(self, user_id: int) -> None:
        user = self.get_by_id(user_id)
        if user:
            self.db_session.delete(user)
            self.db_session.commit()
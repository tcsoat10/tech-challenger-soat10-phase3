from typing import Optional
from sqlalchemy.orm import Session

from src.core.ports.user_profile.i_user_profile_repository import IUserProfileRepository
from src.core.domain.entities.user_profile import UserProfile



class UserProfileRepository(IUserProfileRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, user_profile: UserProfile) -> UserProfile:
        self.db_session.add(user_profile)
        self.db_session.commit()
        return user_profile
    
    def get_by_id(self, id: int) -> UserProfile:
        return self.db_session.query(UserProfile).filter_by(id=id).first()

    def get_by_user_id_and_profile_id(self, user_id: int, profile_id: int) -> UserProfile:
        return self.db_session.query(UserProfile).filter_by(user_id=user_id, profile_id=profile_id).first()
    
    def get_all(self, include_deleted: Optional[bool] = False) -> list[UserProfile]:
        query = self.db_session.query(UserProfile)
        if not include_deleted:
            query = query.filter(UserProfile.inactivated_at.is_(None))
        return query.all()
    
    def update(self, user_profile: UserProfile) -> UserProfile:
        self.db_session.merge(user_profile)
        self.db_session.commit()
        return user_profile
    
    def delete(self, user_profile: UserProfile) -> None:
        user_profile.deleted = True
        self.db_session.commit()

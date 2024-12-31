from src.core.domain.entities.profile import Profile
from src.core.ports.profile.i_profile_repository import IProfileRepository
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from typing import List

class ProfileRepository(IProfileRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, profile: Profile) -> Profile:
        self.db_session.add(profile)
        self.db_session.commit()
        self.db_session.refresh(profile)
        return profile
    
    def exists_by_name(self, name: str) -> bool:
        return self.db_session.query(exists().where(Profile.name == name)).scalar()
    
    def get_by_name(self, name: str) -> Profile:
        return self.db_session.query(Profile).filter(Profile.name == name).first()
    
    def get_by_id(self, profile_id: int) -> Profile:
        return self.db_session.query(Profile).filter(Profile.id == profile_id).first()
    
    def get_all(self) -> List[Profile]:
        return self.db_session.query(Profile).all()
    
    def update(self, profile: Profile) -> Profile:
        self.db_session.merge(profile)
        self.db_session.commit()
        return profile
    
    def delete(self, profile_id: int) -> None:
        profile = self.get_by_id(profile_id=profile_id)
        if profile:
            self.db_session.delete(profile)
            self.db_session.commit()

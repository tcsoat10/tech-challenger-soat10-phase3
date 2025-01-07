from src.core.ports.profile_permission.i_profile_permission_repository import IProfilePermissionRepository
from src.core.domain.entities.profile_permission import ProfilePermission

from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from typing import List


class ProfilePermissionRepository(IProfilePermissionRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def create(self, profile_permission: ProfilePermission) -> ProfilePermission:
        self.db_session.add(profile_permission)
        self.db_session.commit()
        self.db_session.refresh(profile_permission)
        return profile_permission
    
    def exists_by_permission_id_and_profile_id(self, permission_id: int, profile_id: int) -> bool:
        return self.db_session.query(exists().where(ProfilePermission.permission_id == permission_id and ProfilePermission.profile_id == profile_id)).first()
    
    def get_by_id(self, profile_permission_id: int) -> ProfilePermission:
        return self.db_session.query(ProfilePermission).filter(ProfilePermission.id == profile_permission_id).first()
    
    def get_by_permission_id_and_profile_id(self, permission_id: int, profile_id: int) -> ProfilePermission:
        return self.db_session.query(ProfilePermission).filter(ProfilePermission.permission_id == permission_id, ProfilePermission.profile_id == profile_id).first()

    def get_by_profile_id(self, profile_id: int) -> ProfilePermission:
        return self.db_session.query(ProfilePermission).filter(ProfilePermission.profile_id == profile_id).first()
    
    def get_by_permission_id(self, permission_id: int) -> ProfilePermission:
        return self.db_session.query(ProfilePermission).filter(ProfilePermission.permission_id == permission_id).first()
    
    def get_all(self, include_deleted: bool = False) -> List[ProfilePermission]:
        query = self.db_session.query(ProfilePermission)
        if not include_deleted:
            query = query.filter(ProfilePermission.inactivated_at.is_(None))
        return query.all()
    
    def update(self, profile_permission: ProfilePermission) -> ProfilePermission:
        self.db_session.merge(profile_permission)
        self.db_session.commit()
        return profile_permission
    
    def delete(self, profile_permission: ProfilePermission) -> None:
        self.db_session.delete(profile_permission)
        self.db_session.commit()
    

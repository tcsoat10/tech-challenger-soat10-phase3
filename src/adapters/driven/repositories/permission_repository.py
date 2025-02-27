from src.core.domain.entities.permission import Permission
from src.core.ports.permission.i_permission_repository import IPermissionRepository
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from typing import List

class PermissionRepository(IPermissionRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, permission: Permission) -> Permission:
        self.db_session.add(permission)
        self.db_session.commit()
        self.db_session.refresh(permission)
        return permission
    
    def exists_by_name(self, name: str) -> bool:
        return self.db_session.query(exists().where(Permission.name == name)).scalar()
    
    def get_by_name(self, name: str) -> Permission:
        return self.db_session.query(Permission).filter(Permission.name == name).first()
    
    def get_by_id(self, permission_id: int) -> Permission:
        return self.db_session.query(Permission).filter(Permission.id == permission_id).first()
    
    def get_all(self, include_deleted: bool = False) -> List[Permission]:
        query = self.db_session.query(Permission)
        if not include_deleted:
            query = query.filter(Permission.inactivated_at.is_(None))
        return query.all()
    
    def update(self, permission: Permission) -> Permission:
        self.db_session.merge(permission)
        self.db_session.commit()
        return permission
    
    def delete(self, permission_id: int) -> None:
        permission = self.get_by_id(permission_id=permission_id)
        if permission:
            self.db_session.delete(permission)
            self.db_session.commit()

from src.core.domain.entities.permission import Permission
from src.core.ports.permission.i_permission_repository import IPermissionRepository
from sqlalchemy.orm import Session

class PermissionRepository(IPermissionRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, permission: Permission) -> Permission:
        self.db_session.add(permission)
        self.db_session.commit()
        self.db_session.refresh(permission)
        return permission

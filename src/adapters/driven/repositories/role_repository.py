from src.core.ports.role.i_role_repository import IRoleRepository
from src.core.domain.entities.role import Role

from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.sql import exists


class RoleRepository(IRoleRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, role: Role) -> Role:
        self.db_session.add(role)
        self.db_session.commit()
        self.db_session.refresh(role)
        return role
    
    def get_by_name(self, name: str) -> Role:
        return self.db_session.query(Role).filter(Role.name == name).first()
    
    def get_by_id(self, role_id: int) -> Role:
        return self.db_session.query(Role).filter(Role.id == role_id).first()
    
    def get_all(self) -> List[Role]:
        return self.db_session.query(Role).all()
    
    def update(self, role: Role) -> Role:
        self.db_session.merge(role)
        self.db_session.commit()
        return role
    
    def delete(self, role_id: int) -> None:
        role = self.get_by_id(role_id)
        if role:
            self.db_session.delete(role)
            self.db_session.commit()

    def exists_by_name(self, name: str) -> bool:
        return self.db_session.query(exists().where(Role.name == name)).scalar()
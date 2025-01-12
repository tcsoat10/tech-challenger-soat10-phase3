from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.core.domain.entities.base_entity import BaseEntity


class Permission(BaseEntity):
    __tablename__ = "permissions"

    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(300))

    profile_permissions = relationship("ProfilePermission", back_populates="permission")

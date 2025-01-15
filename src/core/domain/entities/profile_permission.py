from src.core.domain.entities.base_entity import BaseEntity
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship


class ProfilePermission(BaseEntity):
    __tablename__ = 'profile_permissions'

    profile_id = Column(ForeignKey('profiles.id'), nullable=False)
    profile = relationship('Profile', back_populates='profile_permissions', overlaps="permissions,profiles")

    permission_id = Column(ForeignKey('permissions.id'), nullable=False)
    permission = relationship('Permission', back_populates='profile_permissions', overlaps="profiles,permissions")

__all__ = ['ProfilePermission']

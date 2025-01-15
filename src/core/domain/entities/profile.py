from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.core.domain.entities.base_entity import BaseEntity


class Profile(BaseEntity):
    __tablename__ = "profiles"

    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(300))

    profile_permissions = relationship("ProfilePermission", back_populates="profile")
    permissions = relationship("Permission", secondary="profile_permissions", back_populates="profiles")

    user_profiles = relationship("UserProfile", back_populates="profile")
    users = relationship("User", secondary="user_profiles", back_populates="profiles")

__all__ = ["Profile"]

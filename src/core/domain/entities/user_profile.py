from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from src.core.domain.entities.base_entity import BaseEntity


class UserProfile(BaseEntity):
    __tablename__ = "user_profiles"

    user_id = Column(ForeignKey("users.id"), nullable=False)
    profile_id = Column(ForeignKey("profiles.id"), nullable=False)

    user = relationship("User", back_populates="user_profiles", overlaps="profiles,users")
    profile = relationship("Profile", back_populates="user_profiles", overlaps="users,profiles")

__all__ = ["UserProfile"]

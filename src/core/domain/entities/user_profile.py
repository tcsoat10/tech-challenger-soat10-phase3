from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.core.domain.entities.base_entity import BaseEntity


class UserProfile(BaseEntity):
    __tablename__ = "user_profiles"

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="user_profiles")

    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)
    profile = relationship("Profile", back_populates="user_profiles")

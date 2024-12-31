from sqlalchemy import Column, String
from src.core.domain.entities.base_entity import BaseEntity


class Profile(BaseEntity):
    __tablename__ = "profiles"

    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(300))

__all__ = ["Profile"]

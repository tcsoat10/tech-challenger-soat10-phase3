from src.core.domain.entities.base_entity import BaseEntity

from sqlalchemy import Column, String


class Role(BaseEntity):
    __tablename__ = 'roles'

    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(100))
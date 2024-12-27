from sqlalchemy import Column, String
from src.core.domain.entities.base_entity import BaseEntity


class Category(BaseEntity):
    __tablename__ = "categories"

    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(300))

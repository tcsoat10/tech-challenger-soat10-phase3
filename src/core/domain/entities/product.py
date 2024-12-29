from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from src.core.domain.entities.base_entity import BaseEntity


class Product(BaseEntity):
    __tablename__ = "products"

    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(300))

    category_id = Column(ForeignKey("categories.id"), nullable=False)
    category = relationship("Category")

    price = Column(Float, nullable=False, default=0.0)
    
    sla_product = Column(String(100), nullable=True)

__all__ = ["Product"]

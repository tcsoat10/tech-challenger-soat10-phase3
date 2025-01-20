from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base
from .base_entity import BaseEntity

Base = declarative_base()

# tabelas
class OrderStatus(BaseEntity):
    __tablename__ = 'order_status'

    status = Column(String(100), unique=True, nullable=False)
    description = Column(String(500), nullable=True)

    __all__ = ['OrderStatus']
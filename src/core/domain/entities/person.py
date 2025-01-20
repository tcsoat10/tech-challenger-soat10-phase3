from src.core.domain.entities.base_entity import BaseEntity
from sqlalchemy import Column, String, Date


class Person(BaseEntity):
    __tablename__ = "persons"

    name = Column(String(100))
    cpf = Column(String(11), unique=True)
    email = Column(String(150), unique=True)
    birth_date = Column(Date)
    
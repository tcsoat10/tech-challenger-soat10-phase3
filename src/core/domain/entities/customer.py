from src.core.domain.entities.base_entity import BaseEntity

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship


class Customer(BaseEntity):
    __tablename__ = 'customers'

    person_id = Column(ForeignKey('persons.id'), nullable=True)
    person = relationship('Person')


__all__ = ['Customer']

from src.core.domain.entities.base_entity import BaseEntity

from sqlalchemy import Column, Date, ForeignKey
from sqlalchemy.orm import relationship


class Employee(BaseEntity):
    __tablename__ = 'employees'

    admission_date = Column(Date)
    termination_date = Column(Date)

    person_id = Column(ForeignKey('persons.id'), nullable=False)
    person = relationship('Person')

    role_id = Column(ForeignKey('roles.id'), nullable=False)
    role = relationship('Role')

    user_id = Column(ForeignKey('users.id'), nullable=False)
    user = relationship('User')


__all__ = ['Employee']

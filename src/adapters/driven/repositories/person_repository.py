from typing import List
from sqlalchemy.sql import exists
from sqlalchemy.orm import Session
from src.core.domain.entities.person import Person
from src.core.ports.person.i_person_repository import IPersonRepository


class PersonRepository(IPersonRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, person: Person) -> Person:
        self.db_session.add(person)
        self.db_session.commit()
        self.db_session.refresh(person)
        return person

    def exists_by_cpf(self, cpf: str) -> bool:
        return self.db_session.query(exists().where(Person.cpf == cpf)).scalar()

    def get_by_cpf(self, cpf: str) -> Person:
        return self.db_session.query(Person).filter(Person.cpf == cpf).first()

    def get_by_id(self, person_id: int) -> Person:
        return self.db_session.query(Person).filter(Person.id == person_id).first()

    def get_all(self, include_deleted: bool = False) -> List[Person]:
        query = self.db_session.query(Person)
        if not include_deleted:
            query = query.filter(Person.inactivated_at.is_(None))
        return query.all()

    def update(self, person: Person) -> Person:
        self.db_session.merge(person)
        self.db_session.commit()
        return person

    def delete(self, person_id: int) -> None:
        person = self.get_by_id(person_id)
        if person:
            self.db_session.delete(person)
            self.db_session.commit()

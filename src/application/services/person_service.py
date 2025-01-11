from typing import List, Optional
from config.database import DELETE_MODE
from src.core.domain.dtos.person.update_person_dto import UpdatePersonDTO
from src.core.domain.dtos.person.create_person_dto import CreatePersonDTO
from src.core.domain.dtos.person.person_dto import PersonDTO
from src.core.domain.entities.person import Person
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.person.i_person_repository import IPersonRepository
from src.core.ports.person.i_person_service import IPersonService


class PersonService(IPersonService):

    def __init__(self, repository: IPersonRepository):
        self.repository = repository
            
    def create_person(self, dto: CreatePersonDTO) -> PersonDTO:
        person = self.repository.get_by_cpf(dto.cpf)
        if person:
            if not person.is_deleted():
                raise EntityDuplicatedException(entity_name='Person')
        else:
            person = Person(name=dto.name, cpf=dto.cpf, email=dto.email, birth_date=dto.birth_date)
            person = self.repository.create(person)
        
        return PersonDTO.from_entity(person)
    
    def get_person_by_cpf(self, cpf: str) -> PersonDTO:
        person = self.repository.get_by_cpf(cpf)
        if not person:
            raise EntityNotFoundException(entity_name="Person")
        return PersonDTO.from_entity(person)

    def get_person_by_id(self, person_id: int) -> PersonDTO:
        person = self.repository.get_by_id(person_id=person_id)
        if not person:
            raise EntityNotFoundException(entity_name="Person")
        return PersonDTO.from_entity(person)

    def get_all_persons(self, include_deleted: Optional[bool] = False) -> List[PersonDTO]:
        person = self.repository.get_all(include_deleted=include_deleted)
        return [PersonDTO.from_entity(person) for person in person]

    def update_person(self, person_id: int, dto: UpdatePersonDTO) -> PersonDTO:
        person = self.repository.get_by_id(person_id)
        if not person:
            raise EntityDuplicatedException(entity_name="Person")

        person.cpf=dto.cpf,
        person.name=dto.name,
        person.email=dto.email,
        person.birth_date=dto.birth_date
        
        person = self.repository.update(person)

        return PersonDTO.from_entity(person)

    def delete_person(self, person_id: int) -> None:
        person = self.repository.get_by_id(person_id)
        if not person:
            raise EntityNotFoundException(entity_name="Person")
        
        if DELETE_MODE == 'soft':
            if person.is_deleted():
                raise EntityNotFoundException(entity_name="Person")

            person.soft_delete()
            self.repository.update(person)
        else:
            self.repository.delete(person)

__all__ = ["PersonService"]

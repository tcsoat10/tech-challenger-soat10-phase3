from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db
from src.core.domain.dtos.person.update_person_dto import UpdatePersonDTO
from src.adapters.driven.repositories.person_repository import PersonRepository
from src.application.services.person_service import PersonService
from src.core.domain.dtos.person.person_dto import PersonDTO
from src.core.domain.dtos.person.create_person_dto import CreatePersonDTO
from src.core.ports.person.i_person_repository import IPersonRepository
from src.core.ports.person.i_person_service import IPersonService

router = APIRouter()

# Substituir por lib DI.
def _get_person_service(db_session: Session = Depends(get_db)) -> IPersonService:
    repository: IPersonRepository = PersonRepository(db_session)
    return PersonService(repository)


@router.post("/person", response_model=PersonDTO, status_code=status.HTTP_201_CREATED)
def create_person(dto: CreatePersonDTO, service: IPersonService = Depends(_get_person_service)):
    return service.create_person(dto)


@router.get("/person/{cpf}/cpf", response_model=PersonDTO, status_code=status.HTTP_200_OK)
def get_person_by_cpf(cpf: str, service: IPersonService = Depends(_get_person_service)):
    return service.get_person_by_cpf(cpf)


@router.get("/person/{person_id}/id", response_model=PersonDTO, status_code=status.HTTP_200_OK)
def get_person_by_id(person_id: int, service: IPersonService = Depends(_get_person_service)):
    return service.get_person_by_id(person_id=person_id)


@router.get("/person", response_model=List[PersonDTO])
def get_all_person(service: IPersonService = Depends(_get_person_service)):
    return service.get_all_persons()


@router.put("/person/{person_id}", response_model=PersonDTO)
def update_person(person_id: int, dto: UpdatePersonDTO, service: IPersonService = Depends(_get_person_service)):
    return service.update_person(person_id, dto)


@router.delete("/person/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(person_id: int, service: IPersonService = Depends(_get_person_service)):
    service.delete_person(person_id)

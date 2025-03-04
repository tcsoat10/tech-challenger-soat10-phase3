from typing import List
from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.orm import Session

from config.database import get_db
from src.constants.permissions import PersonPermissions
from src.core.auth.dependencies import get_current_user
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


@router.post(
    "/person",
    response_model=PersonDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=[PersonPermissions.CAN_CREATE_PERSON])]
)
def create_person(
    dto: CreatePersonDTO,
    service: IPersonService = Depends(_get_person_service),
    user=Depends(get_current_user)
):
    return service.create_person(dto)


@router.get(
    "/person/{cpf}/cpf",
    response_model=PersonDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[PersonPermissions.CAN_VIEW_PERSONS])]
)
def get_person_by_cpf(
    cpf: str,
    service: IPersonService = Depends(_get_person_service),
    user=Depends(get_current_user)
):
    return service.get_person_by_cpf(cpf)


@router.get(
    "/person/{person_id}/id",
    response_model=PersonDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[PersonPermissions.CAN_VIEW_PERSONS])]
)
def get_person_by_id(
    person_id: int,
    service: IPersonService = Depends(_get_person_service),
    user=Depends(get_current_user)
):
    return service.get_person_by_id(person_id=person_id)


@router.get(
    "/person",
    response_model=List[PersonDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[PersonPermissions.CAN_VIEW_PERSONS])]
)
def get_all_person(
    service: IPersonService = Depends(_get_person_service),
    user=Depends(get_current_user)
):
    return service.get_all_persons()


@router.put(
    "/person/{person_id}",
    response_model=PersonDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[PersonPermissions.CAN_UPDATE_PERSON])]
)
def update_person(
    person_id: int,
    dto: UpdatePersonDTO,
    service: IPersonService = Depends(_get_person_service),
    user=Depends(get_current_user)
):
    return service.update_person(person_id, dto)


# @router.delete(
#     "/person/{person_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     dependencies=[Security(get_current_user, scopes=[PersonPermissions.CAN_DELETE_PERSON])]
# )
# def delete_person(
#     person_id: int,
#     service: IPersonService = Depends(_get_person_service),
#     user=Depends(get_current_user)
# ):
#     service.delete_person(person_id)

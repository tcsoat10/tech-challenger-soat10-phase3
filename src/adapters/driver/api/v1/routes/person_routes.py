from typing import List, Optional
from fastapi import APIRouter, Depends, Security, status
from sqlalchemy.orm import Session

from src.adapters.driven.repositories.person_repository import PersonRepository
from config.database import get_db
from src.core.ports.person.i_person_repository import IPersonRepository
from src.constants.permissions import PersonPermissions
from src.core.auth.dependencies import get_current_user
from src.core.domain.dtos.person.update_person_dto import UpdatePersonDTO
from src.core.domain.dtos.person.person_dto import PersonDTO
from src.core.domain.dtos.person.create_person_dto import CreatePersonDTO
from src.adapters.driver.api.v1.controllers.person_controller import PersonController


router = APIRouter()


def _get_person_controller(db_session: Session = Depends(get_db)) -> PersonController:
    person_gateway: IPersonRepository = PersonRepository(db_session)
    return PersonController(person_gateway)


@router.post(
    "/person",
    response_model=PersonDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=[PersonPermissions.CAN_CREATE_PERSON])]
)
def create_person(
    dto: CreatePersonDTO,
    controller: PersonController = Depends(_get_person_controller),
    user=Depends(get_current_user)
):
    return controller.create_person(dto)


@router.get(
    "/person/{cpf}/cpf",
    response_model=PersonDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[PersonPermissions.CAN_VIEW_PERSONS])]
)
def get_person_by_cpf(
    cpf: str,
    controller: PersonController = Depends(_get_person_controller),
    user=Depends(get_current_user)
):
    return controller.get_person_by_cpf(cpf)


@router.get(
    "/person/{person_id}/id",
    response_model=PersonDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[PersonPermissions.CAN_VIEW_PERSONS])]
)
def get_person_by_id(
    person_id: int,
    controller: PersonController = Depends(_get_person_controller),
    user=Depends(get_current_user)
):
    return controller.get_person_by_id(person_id=person_id)


@router.get(
    "/person",
    response_model=List[PersonDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[PersonPermissions.CAN_VIEW_PERSONS])]
)
def get_all_person(
    include_deleted: Optional[bool] = False,
    controller: PersonController = Depends(_get_person_controller),
    user=Depends(get_current_user)
):
    return controller.get_all_persons(include_deleted)


@router.put(
    "/person/{person_id}",
    response_model=PersonDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[PersonPermissions.CAN_UPDATE_PERSON])]
)
def update_person(
    person_id: int,
    dto: UpdatePersonDTO,
    controller: PersonController = Depends(_get_person_controller),
    user=Depends(get_current_user)
):
    return controller.update_person(person_id, dto)


@router.delete(
    "/person/{person_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=[PersonPermissions.CAN_DELETE_PERSON])]
)
def delete_person(
    person_id: int,
    controller: PersonController = Depends(_get_person_controller),
    user=Depends(get_current_user)
):
    controller.delete_person(person_id)

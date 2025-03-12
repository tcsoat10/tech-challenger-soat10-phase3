from fastapi import APIRouter, Depends, status, Security
from sqlalchemy.orm import Session
from typing import List, Optional

from src.adapters.driven.repositories.employee_repository import EmployeeRepository
from src.adapters.driven.repositories.person_repository import PersonRepository
from src.adapters.driven.repositories.role_repository import RoleRepository
from src.adapters.driven.repositories.user_repository import UserRepository
from config.database import get_db
from src.core.ports.employee.i_employee_repository import IEmployeeRepository
from src.core.ports.person.i_person_repository import IPersonRepository
from src.core.ports.role.i_role_repository import IRoleRepository
from src.core.ports.user.i_user_repository import IUserRepository
from src.adapters.driver.api.v1.controllers.employee_controller import EmployeeController
from src.core.domain.dtos.employee.employee_dto import EmployeeDTO
from src.core.domain.dtos.employee.create_employee_dto import CreateEmployeeDTO
from src.core.domain.dtos.employee.update_employee_dto import UpdateEmployeeDTO
from src.core.auth.dependencies import get_current_user
from src.constants.permissions import EmployeePermissions


router = APIRouter()

def _get_employee_controller(db_session: Session = Depends(get_db)) -> EmployeeController:
    employee_gateway: IEmployeeRepository = EmployeeRepository(db_session)
    person_gateway: IPersonRepository = PersonRepository(db_session)
    role_gateway: IRoleRepository = RoleRepository(db_session)
    user_gateway: IUserRepository = UserRepository(db_session)
    return EmployeeController(employee_gateway, person_gateway, role_gateway, user_gateway)

@router.post(
        '/employees',
        response_model=EmployeeDTO,
        status_code=status.HTTP_201_CREATED,
        dependencies=[Security(get_current_user, scopes=[EmployeePermissions.CAN_CREATE_EMPLOYEE])]
)
def create_employee(
    dto: CreateEmployeeDTO,
    controller: EmployeeController = Depends(_get_employee_controller),
    user: dict = Security(get_current_user)
):
    return controller.create_employee(dto)


@router.get(
        '/employees/{employee_id}/id',
        response_model=EmployeeDTO,
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[EmployeePermissions.CAN_VIEW_EMPLOYEES])]
)
def get_employee_by_id(
    employee_id: int,
    controller: EmployeeController = Depends(_get_employee_controller),
    user: dict = Security(get_current_user)
):
    return controller.get_employee_by_id(employee_id)


@router.get(
        '/employees/{person_id}/person_id',
        response_model=EmployeeDTO,
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[EmployeePermissions.CAN_VIEW_EMPLOYEES])]
)
def get_employee_by_person_id(
    person_id: int,
    controller: EmployeeController = Depends(_get_employee_controller),
    user: dict = Security(get_current_user)
):
    return controller.get_employee_by_person_id(person_id)


@router.get(
        '/employees/{user_id}/user_id',
        response_model=EmployeeDTO,
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[EmployeePermissions.CAN_VIEW_EMPLOYEES])]
)
def get_employee_by_user_id(
    user_id: int,
    controller: EmployeeController = Depends(_get_employee_controller),
    user: dict = Security(get_current_user)
):
    return controller.get_employee_by_user_id(user_id)


@router.get(
        '/employees/{role_id}/role_id',
        response_model=List[EmployeeDTO],
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[EmployeePermissions.CAN_VIEW_EMPLOYEES])]
)
def list_employees_by_role_id(
    role_id: int,
    controller: EmployeeController = Depends(_get_employee_controller),
    user: dict = Security(get_current_user)
):
    return controller.list_employees_by_role_id(role_id)


@router.get(
        '/employees',
        response_model=List[EmployeeDTO],
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[EmployeePermissions.CAN_VIEW_EMPLOYEES])]
)
def get_all_employees(
    include_deleted: Optional[bool] = False,
    controller: EmployeeController = Depends(_get_employee_controller),
    user: dict = Security(get_current_user)
):
    return controller.get_all_employees(include_deleted=include_deleted)


@router.put(
        '/employees/{employee_id}',
        response_model=EmployeeDTO,
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[EmployeePermissions.CAN_UPDATE_EMPLOYEE])]
)
def update_employee(
    employee_id: int,
    dto: UpdateEmployeeDTO,
    controller: EmployeeController = Depends(_get_employee_controller),
    user: dict = Security(get_current_user)
):
    return controller.update_employee(employee_id, dto)


@router.delete(
        '/employees/{employee_id}',
        status_code=status.HTTP_204_NO_CONTENT,
        dependencies=[Security(get_current_user, scopes=[EmployeePermissions.CAN_DELETE_EMPLOYEE])]
)
def delete_employee(
    employee_id: int,
    controller: EmployeeController = Depends(_get_employee_controller),
    user: dict = Security(get_current_user)
):
    return controller.delete_employee(employee_id)
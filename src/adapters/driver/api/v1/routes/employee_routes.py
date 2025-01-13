from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional

from config.database import get_db
from src.core.ports.employee.i_employee_service import IEmployeeService
from src.core.ports.employee.i_employee_repository import IEmployeeRepository
from src.adapters.driven.repositories.employee_repository import EmployeeRepository
from src.core.ports.person.i_person_repository import IPersonRepository
from src.adapters.driven.repositories.person_repository import PersonRepository
from src.core.ports.role.i_role_repository import IRoleRepository
from src.adapters.driven.repositories.role_repository import RoleRepository
from src.core.ports.user.i_user_repository import IUserRepository
from src.adapters.driven.repositories.user_repository import UserRepository
from src.application.services.employee_service import EmployeeService
from src.core.domain.dtos.employee.employee_dto import EmployeeDTO
from src.core.domain.dtos.employee.create_employee_dto import CreateEmployeeDTO
from src.core.domain.dtos.employee.update_employee_dto import UpdateEmployeeDTO



router = APIRouter()


def _get_employee_service(db_session: Session = Depends(get_db)) -> IEmployeeService:
    employee_repository: IEmployeeRepository = EmployeeRepository(db_session)
    person_repository: IPersonRepository = PersonRepository(db_session)
    role_repository: IRoleRepository = RoleRepository(db_session)
    user_repository: IUserRepository = UserRepository(db_session)
    return EmployeeService(employee_repository, person_repository, role_repository, user_repository)


@router.post('/employees', response_model=EmployeeDTO, status_code=status.HTTP_201_CREATED)
def create_employee(dto: CreateEmployeeDTO, service: IEmployeeService = Depends(_get_employee_service)):
    return service.create_employee(dto)


@router.get('/employees/{employee_id}/id', response_model=EmployeeDTO, status_code=status.HTTP_200_OK)
def get_employee_by_id(employee_id: int, service: IEmployeeService = Depends(_get_employee_service)):
    return service.get_employee_by_id(employee_id)


@router.get('/employees/{person_id}/person_id', response_model=EmployeeDTO, status_code=status.HTTP_200_OK)
def get_employee_by_person_id(person_id: int, service: IEmployeeService = Depends(_get_employee_service)):
    return service.get_employee_by_person_id(person_id)


@router.get('/employees/{user_id}/user_id', response_model=EmployeeDTO, status_code=status.HTTP_200_OK)
def get_employee_by_user_id(user_id: int, service: IEmployeeService = Depends(_get_employee_service)):
    return service.get_employee_by_user_id(user_id)


@router.get('/employees/{role_id}/role_id', response_model=List[EmployeeDTO], status_code=status.HTTP_200_OK)
def get_employees_by_role_id(role_id: int, service: IEmployeeService = Depends(_get_employee_service)):
    return service.get_employees_by_role_id(role_id)


@router.get('/employees', response_model=List[EmployeeDTO], status_code=status.HTTP_200_OK)
def get_all_employees(include_deleted: Optional[bool] = False, service: IEmployeeService = Depends(_get_employee_service)):
    return service.get_all_employees(include_deleted=include_deleted)


@router.put('/employees/{employee_id}', response_model=EmployeeDTO, status_code=status.HTTP_200_OK)
def update_employee(employee_id: int, dto: UpdateEmployeeDTO, service: IEmployeeService = Depends(_get_employee_service)):
    return service.update_employee(employee_id, dto)


@router.delete('/employees/{employee_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, service: IEmployeeService = Depends(_get_employee_service)):
    return service.delete_employee(employee_id)
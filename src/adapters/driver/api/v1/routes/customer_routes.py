from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional

from config.database import get_db
from src.core.ports.customer.i_customer_service import ICustomerService
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.adapters.driven.repositories.customer_repository import CustomerRepository
from src.core.ports.person.i_person_repository import IPersonRepository
from src.adapters.driven.repositories.person_repository import PersonRepository
from src.application.services.customer_service import CustomerService
from src.core.domain.dtos.customer.customer_dto import CustomerDTO
from src.core.domain.dtos.customer.create_customer_dto import CreateCustomerDTO
from src.core.domain.dtos.customer.update_customer_dto import UpdateCustomerDTO


router = APIRouter()


def _get_customer_service(db_session: Session = Depends(get_db)) -> ICustomerService:
    customer_repository: ICustomerRepository = CustomerRepository(db_session)
    person_repository: IPersonRepository = PersonRepository(db_session)
    return CustomerService(customer_repository, person_repository)


@router.post('/customers', response_model=CustomerDTO, status_code=status.HTTP_201_CREATED)
def create_customer(dto: CreateCustomerDTO, service: ICustomerService = Depends(_get_customer_service)):
    return service.create_customer(dto)


@router.get('/customers/{customer_id}/id', response_model=CustomerDTO, status_code=status.HTTP_200_OK)
def get_customer_by_id(customer_id: int, service: ICustomerService = Depends(_get_customer_service)):
    return service.get_customer_by_id(customer_id)


@router.get('/customers/{person_id}/person_id', response_model=CustomerDTO, status_code=status.HTTP_200_OK)
def get_customer_by_id(person_id: int, service: ICustomerService = Depends(_get_customer_service)):
    return service.get_customer_by_person_id(person_id)


@router.get('/customers', response_model=List[CustomerDTO], status_code=status.HTTP_200_OK)
def get_all_customers(include_deleted: Optional[bool] = False, service: ICustomerService = Depends(_get_customer_service)):
    return service.get_all_customers(include_deleted=include_deleted)


@router.put('/customers/{customer_id}', response_model=CustomerDTO, status_code=status.HTTP_200_OK)
def update_customer(customer_id: int, dto: UpdateCustomerDTO, service: ICustomerService = Depends(_get_customer_service)):
    return service.update_customer(customer_id, dto)


@router.delete('/customers/{customer_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, service: ICustomerService = Depends(_get_customer_service)):
    service.delete_customer(customer_id)
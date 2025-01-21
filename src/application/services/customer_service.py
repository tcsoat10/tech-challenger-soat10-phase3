from src.core.domain.entities.person import Person
from src.core.ports.customer.i_customer_service import ICustomerService
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.ports.person.i_person_repository import IPersonRepository
from src.core.domain.dtos.customer.create_customer_dto import CreateCustomerDTO
from src.core.domain.dtos.customer.customer_dto import CustomerDTO
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.domain.entities.customer import Customer
from src.core.domain.dtos.customer.update_customer_dto import UpdateCustomerDTO
from config.database import DELETE_MODE

from typing import List, Optional


class CustomerService(ICustomerService):
    def __init__(self, repository: ICustomerRepository, person_repository: IPersonRepository):
        self.repository = repository
        self.person_repository = person_repository

    def _is_customer(self, current_user: dict) -> bool:
        return current_user['profile']['name'] in ['customer']
    
    def create_customer(self, dto: CreateCustomerDTO) -> CustomerDTO:
        person = self.person_repository.get_by_cpf(dto.person.cpf)
        if not person:
            if self.person_repository.exists_by_email(dto.person.email):
                raise EntityDuplicatedException(entity_name='Customer')

            person = Person(
                name=dto.person.name,
                cpf=dto.person.cpf,
                email=dto.person.email,
                birth_date=dto.person.birth_date
            )
            person = self.person_repository.create(person)
        else:
            person.name = dto.person.name
            person.email = dto.person.email
            person.birth_date = dto.person.birth_date
            if person.is_deleted():
                person.reactivate()
            self.person_repository.update(person)

        customer = self.repository.get_by_person_id(person.id)
        if customer:
            if not customer.is_deleted():
                raise EntityDuplicatedException(entity_name='Customer')
            customer.reactivate()
            customer.person_id = person.id
            customer = self.repository.update(customer)
        else:
            customer = Customer(person_id=person.id)
            customer = self.repository.create(customer)

        return CustomerDTO.from_entity(customer)
    
    def get_customer_by_id(self, customer_id: int, current_user: dict) -> CustomerDTO:
        if self._is_customer(current_user) and int(current_user['person']['id']) != customer_id:
            raise EntityNotFoundException(entity_name='Customer')

        customer = self.repository.get_by_id(customer_id)
        if not customer:
            raise EntityNotFoundException(entity_name='Customer')
        return CustomerDTO.from_entity(customer)
    
    def get_customer_by_person_id(self, person_id: int, current_user: dict) -> CustomerDTO:
        customer = self.repository.get_by_person_id(person_id)
        if not customer:
            raise EntityNotFoundException(entity_name='Customer')
        
        if self._is_customer(current_user) and int(current_user['person']['id']) != customer.id:
            raise EntityNotFoundException(entity_name='Customer')
        
        return CustomerDTO.from_entity(customer)

    def get_all_customers(self, current_user: dict, include_deleted: Optional[bool] = False) -> List[CustomerDTO]:
        customers = self.repository.get_all(include_deleted=include_deleted)
        
        if self._is_customer(current_user):
            customers = [customer for customer in customers if customer.id == int(current_user['person']['id'])]

        return [CustomerDTO.from_entity(customer) for customer in customers]
    
    def update_customer(self, customer_id: int, dto: UpdateCustomerDTO, current_user: dict) -> CustomerDTO:
        if self._is_customer(current_user) and int(current_user['person']['id']) != customer_id:
            raise EntityNotFoundException(entity_name='Customer')

        customer = self.repository.get_by_id(customer_id)
        if not customer:
            raise EntityNotFoundException(entity_name='Customer')
        
        if customer.is_deleted():
            raise EntityNotFoundException(entity_name='Customer')
        
        if customer.person.cpf != dto.person.cpf:
            raise EntityNotFoundException(entity_name='Person')

        person = self.person_repository.get_by_id(customer.person_id)
        if not person:
            raise EntityNotFoundException(entity_name='Person')

        person.cpf = dto.person.cpf
        person.name = dto.person.name
        person.email = dto.person.email
        person.birth_date = dto.person.birth_date

        self.person_repository.update(person)

        customer.person_id = person.id
        customer = self.repository.update(customer)

        return CustomerDTO.from_entity(customer)
    
    def delete_customer(self, customer_id: int, current_user: dict) -> None:
        if self._is_customer(current_user) and int(current_user['person']['id']) != customer_id:
            raise EntityNotFoundException(entity_name='Customer')

        customer = self.repository.get_by_id(customer_id)
        if not customer:
            raise EntityNotFoundException(entity_name='Customer')
        if customer.is_deleted():
                raise EntityNotFoundException(entity_name='Customer')
        if DELETE_MODE == 'soft':
            if customer.is_deleted():
                raise EntityNotFoundException(entity_name='Customer')
            customer.soft_delete()
            self.repository.update(customer)
        else:
            self.repository.delete(customer_id)

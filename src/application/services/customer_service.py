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
    
    def create_customer(self, dto: CreateCustomerDTO) -> CustomerDTO:
        person = self.person_repository.get_by_id(dto.person_id)
        if not person:
            raise EntityNotFoundException(entity_name='Person')
        
        customer = self.repository.get_by_person_id(dto.person_id)
        if customer:
            if not customer.is_deleted():
                raise EntityDuplicatedException(entity_name='Customer')
            
            customer.person = person
            customer.reactivate()
            self.repository.update(customer)
        else:
            customer = Customer(person=person)
            customer = self.repository.create(customer)

        return CustomerDTO.from_entity(customer)
    
    def get_customer_by_id(self, customer_id: int) -> CustomerDTO:
        customer = self.repository.get_by_id(customer_id)
        if not customer:
            raise EntityNotFoundException(entity_name='Customer')
        return CustomerDTO.from_entity(customer)
    
    def get_customer_by_person_id(self, person_id: int) -> CustomerDTO:
        customer = self.repository.get_by_person_id(person_id)
        if not customer:
            raise EntityNotFoundException(entity_name='Customer')
        return CustomerDTO.from_entity(customer)

    def get_all_customers(self, include_deleted: Optional[bool] = False) -> List[CustomerDTO]:
        customers = self.repository.get_all(include_deleted=include_deleted)
        return [CustomerDTO.from_entity(customer) for customer in customers]
    
    def update_customer(self, customer_id: int, dto: UpdateCustomerDTO) -> CustomerDTO:
        customer = self.repository.get_by_id(customer_id)
        if not customer:
            raise EntityNotFoundException(entity_name='Customer')
        
        person = self.person_repository.get_by_id(dto.person_id)
        if not person:
            raise EntityNotFoundException(entity_name='Person')
        
        customer.person = person

        customer = self.repository.update(customer)

        return CustomerDTO.from_entity(customer)
    
    def delete_customer(self, customer_id: int) -> None:
        customer = self.repository.get_by_id(customer_id)
        if not customer:
            raise EntityNotFoundException(entity_name='Customer')
        
        if DELETE_MODE == 'soft':
            if customer.is_deleted():
                raise EntityNotFoundException(entity_name='Customer')
            customer.soft_delete()
            self.repository.update(customer)
        else:
            self.repository.delete(customer_id)
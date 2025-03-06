from sqlalchemy.orm import Session
from typing import Optional, List


from src.core.ports.person.i_person_repository import IPersonRepository
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.adapters.driven.repositories.customer_repository import CustomerRepository
from src.adapters.driven.repositories.person_repository import PersonRepository
from src.core.domain.dtos.customer.create_customer_dto import CreateCustomerDTO
from src.core.domain.dtos.customer.customer_dto import CustomerDTO
from src.application.usecases.customer_usecase.create_customer_usecase import CreateCustomerUsecase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.customer_usecase.get_customer_by_id_usecase import GetCustomerByIdUsecase
from src.application.usecases.customer_usecase.get_customer_by_person_id_usecase import GetCustomerByPersonIdUsecase
from src.application.usecases.customer_usecase.get_all_customers_usecase import GetAllCustomersUsecase


class CustomerController:
    def __init__(self, db_connection: Session):
        self.customer_gateway: ICustomerRepository = CustomerRepository(db_connection)
        self.person_gateway: IPersonRepository = PersonRepository(db_connection)

    def create_customer(self, dto: CreateCustomerDTO) -> CustomerDTO:
        create_customer_usecase = CreateCustomerUsecase.build(self.customer_gateway, self.person_gateway)
        customer = create_customer_usecase.execute(dto)
        return DTOPresenter.transform(customer, CustomerDTO)
    
    def get_customer_by_id(self, customer_id: int, current_user: dict) -> CustomerDTO:
        customer_by_id_usecase = GetCustomerByIdUsecase.build(self.customer_gateway)
        customer = customer_by_id_usecase.execute(customer_id, current_user)
        return DTOPresenter.transform(customer, CustomerDTO)

    def get_customer_by_person_id(self, person_id: int, current_user: dict) -> CustomerDTO:
        customer_by_person_id_usecase = GetCustomerByPersonIdUsecase.build(self.customer_gateway)
        customer = customer_by_person_id_usecase.execute(person_id, current_user)
        return DTOPresenter.transform(customer, CustomerDTO)
    
    def get_all_customers(self, current_user: dict, include_deleted: Optional[bool] = False) -> List[CustomerDTO]:
        all_customers_usecase = GetAllCustomersUsecase.build(self.customer_gateway)
        customers = all_customers_usecase.execute(current_user, include_deleted)
        return DTOPresenter.transform_list(customers, CustomerDTO)
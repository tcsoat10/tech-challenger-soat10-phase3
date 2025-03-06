from sqlalchemy.orm import Session


from src.core.ports.person.i_person_repository import IPersonRepository
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.adapters.driven.repositories.customer_repository import CustomerRepository
from src.adapters.driven.repositories.person_repository import PersonRepository
from src.core.domain.dtos.customer.create_customer_dto import CreateCustomerDTO
from src.core.domain.dtos.customer.customer_dto import CustomerDTO
from src.application.usecases.customer_usecase.create_customer_usecase import CreateCustomerUsecase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter


class CustomerController:
    def __init__(self, db_connection: Session):
        self.customer_gateway: ICustomerRepository = CustomerRepository(db_connection)
        self.person_gateway: IPersonRepository = PersonRepository(db_connection)

    def create_customer(self, dto: CreateCustomerDTO) -> CustomerDTO:
        create_customer_usecase = CreateCustomerUsecase.build(self.customer_gateway, self.person_gateway)
        customer = create_customer_usecase.execute(dto)
        return DTOPresenter.transform(customer, CustomerDTO)
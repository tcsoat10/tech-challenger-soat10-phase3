
from sqlalchemy.orm import Session

from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.auth_usecase.login_customer_by_cpf_usecase import LoginCustomerByCpfUseCase
from src.adapters.driven.repositories.customer_repository import CustomerRepository
from src.adapters.driven.repositories.employee_repository import EmployeeRepository
from src.adapters.driven.repositories.profile_repository import ProfileRepository
from src.core.domain.dtos.auth.auth_dto import AuthByCpfDTO, TokenDTO
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.ports.employee.i_employee_repository import IEmployeeRepository
from src.core.ports.profile.i_profile_repository import IProfileRepository

class AuthController:
    
    def __init__(self, db_session: Session):
        self.profile_gateway: IProfileRepository = ProfileRepository(db_session)
        self.employee_gateway: IEmployeeRepository = EmployeeRepository(db_session)
        self.customer_gateway: ICustomerRepository = CustomerRepository(db_session)
        
    def login_customer_by_cpf(self, dto: AuthByCpfDTO) -> TokenDTO:
        login_customer_by_cpf_use_case = LoginCustomerByCpfUseCase.build(self.customer_gateway, self.profile_gateway)
        token = login_customer_by_cpf_use_case.execute(dto)
        return DTOPresenter.transform_from_dict(token, TokenDTO)

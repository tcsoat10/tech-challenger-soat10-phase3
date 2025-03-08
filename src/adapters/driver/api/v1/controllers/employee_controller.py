
from sqlalchemy.orm import Session

from src.adapters.driven.repositories.person_repository import PersonRepository
from src.adapters.driven.repositories.role_repository import RoleRepository
from src.adapters.driven.repositories.user_repository import UserRepository
from src.core.ports.person.i_person_repository import IPersonRepository
from src.core.ports.role.i_role_repository import IRoleRepository
from src.core.ports.user.i_user_repository import IUserRepository
from src.application.usecases.employee_usecase.create_employee_usecase import CreateEmployeeUseCase
from src.adapters.driven.repositories.employee_repository import EmployeeRepository
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.core.domain.dtos.employee.create_employee_dto import CreateEmployeeDTO
from src.core.domain.dtos.employee.employee_dto import EmployeeDTO
from src.core.ports.employee.i_employee_repository import IEmployeeRepository

class EmployeeController:
    
    def __init__(self, db_session: Session):
        self.employee_gateway: IEmployeeRepository = EmployeeRepository(db_session)
        self.person_gateway: IPersonRepository = PersonRepository(db_session)
        self.role_gateway: IRoleRepository = RoleRepository(db_session)
        self.user_gateway: IUserRepository = UserRepository(db_session)
        
    def create_employee(self, dto: CreateEmployeeDTO) -> EmployeeDTO:
        create_employee_use_case = CreateEmployeeUseCase.build(
            self.employee_gateway,
            self.person_gateway,
            self.role_gateway,
            self.user_gateway
        )
        employee = create_employee_use_case.execute(dto)
        return DTOPresenter.transform(employee, EmployeeDTO)

from fastapi import APIRouter, Depends
from src.adapters.driven.repositories.employee_repository import EmployeeRepository
from src.adapters.driven.repositories.profile_repository import ProfileRepository
from src.adapters.driven.repositories.customer_repository import CustomerRepository
from src.core.ports.employee.i_employee_repository import IEmployeeRepository
from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.core.ports.auth.i_auth_service import IAuthService
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.domain.dtos.auth.auth_dto import AuthByCpfDTO, LoginDTO, TokenDTO
from src.application.services.auth_service import AuthService

router = APIRouter()

def _get_auth_service() -> IAuthService:
    employee_repository: IEmployeeRepository = EmployeeRepository()
    customer_repository: ICustomerRepository = CustomerRepository()
    profile_repository: IProfileRepository = ProfileRepository()
    return AuthService(customer_repository, profile_repository, employee_repository)

@router.post("/auth/customer/cpf", response_model=TokenDTO)
def login_customer_cpf(dto: AuthByCpfDTO, auth_service: IAuthService = Depends(_get_auth_service)):
    token = auth_service.login_customer_by_cpf(dto)
    return token

@router.post("/auth/employee", response_model=TokenDTO)
def login_employee(dto: LoginDTO, auth_service: IAuthService = Depends(_get_auth_service)):
    token = auth_service.login_employee(dto)
    return token

@router.post("/auth/customer/anonymous", response_model=TokenDTO)
def login_anonymous(auth_service: IAuthService = Depends(_get_auth_service)):
    token = auth_service.login_anonymous()
    return token

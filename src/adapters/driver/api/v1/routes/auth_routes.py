from typing import Annotated
from fastapi import APIRouter, Depends
from config.database import get_db
from sqlalchemy.orm import Session

from src.adapters.driver.api.v1.controllers.auth_controller import AuthController
from src.core.auth.oauth2_password_request_form_custom import OAuth2PasswordRequestFormCustom
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

def _get_auth_service(db_session: Session = Depends(get_db)) -> IAuthService:
    employee_repository: IEmployeeRepository = EmployeeRepository(db_session)
    customer_repository: ICustomerRepository = CustomerRepository(db_session)
    profile_repository: IProfileRepository = ProfileRepository(db_session)
    return AuthService(customer_repository, profile_repository, employee_repository)

def _get_auth_controller(db_session: Session = Depends(get_db)) -> AuthController:
    return AuthController(db_session)

@router.post("/auth/token", response_model=TokenDTO)
def get_oauth_token(
    form_data: Annotated[OAuth2PasswordRequestFormCustom, Depends()],
    auth_service: AuthService = Depends(_get_auth_service),
    auth_controller: AuthController = Depends(_get_auth_controller)
):
    if form_data.username and form_data.password:
        return auth_service.login_employee(LoginDTO(username=form_data.username, password=form_data.password))
    elif form_data.username:
        return auth_controller.login_customer_by_cpf(AuthByCpfDTO(cpf=form_data.username))
   
    return auth_controller.login_customer_anonymous()

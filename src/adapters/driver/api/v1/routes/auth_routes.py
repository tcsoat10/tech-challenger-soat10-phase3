from typing import Annotated
from fastapi import APIRouter, Depends
from src.adapters.driven.repositories.customer_repository import CustomerRepository
from src.adapters.driven.repositories.employee_repository import EmployeeRepository
from src.adapters.driven.repositories.profile_repository import ProfileRepository
from config.database import get_db
from sqlalchemy.orm import Session

from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.ports.employee.i_employee_repository import IEmployeeRepository
from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.adapters.driver.api.v1.controllers.auth_controller import AuthController
from src.core.auth.oauth2_password_request_form_custom import OAuth2PasswordRequestFormCustom
from src.core.domain.dtos.auth.auth_dto import AuthByCpfDTO, LoginDTO, TokenDTO

router = APIRouter()

def _get_auth_controller(db_session: Session = Depends(get_db)) -> AuthController:
    profile_gateway: IProfileRepository = ProfileRepository(db_session)
    employee_gateway: IEmployeeRepository = EmployeeRepository(db_session)
    customer_gateway: ICustomerRepository = CustomerRepository(db_session)
    return AuthController(profile_gateway, employee_gateway, customer_gateway)
    

@router.post("/auth/token", response_model=TokenDTO)
def get_oauth_token(
    form_data: Annotated[OAuth2PasswordRequestFormCustom, Depends()],
    auth_controller: AuthController = Depends(_get_auth_controller)
):
    if form_data.username and form_data.password:
        return auth_controller.login_employee(LoginDTO(username=form_data.username, password=form_data.password))
    elif form_data.username:
        return auth_controller.login_customer_by_cpf(AuthByCpfDTO(cpf=form_data.username))
   
    return auth_controller.login_customer_anonymous()

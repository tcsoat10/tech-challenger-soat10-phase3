from typing import Annotated
from fastapi import APIRouter, Depends
from config.database import get_db
from sqlalchemy.orm import Session

from src.adapters.driver.api.v1.controllers.auth_controller import AuthController
from src.core.auth.oauth2_password_request_form_custom import OAuth2PasswordRequestFormCustom
from src.core.domain.dtos.auth.auth_dto import AuthByCpfDTO, LoginDTO, TokenDTO

router = APIRouter()

def _get_auth_controller(db_session: Session = Depends(get_db)) -> AuthController:
    return AuthController(db_session)

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

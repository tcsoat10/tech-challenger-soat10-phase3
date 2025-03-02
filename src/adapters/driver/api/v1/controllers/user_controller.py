from src.core.ports.user.i_user_repository import IUserRepository
from src.adapters.driven.repositories.user_repository import UserRepository
from src.core.domain.dtos.user.create_user_dto import CreateUserDTO
from src.core.domain.dtos.user.user_dto import UserDTO
from src.application.usecases.user_usecase.create_user_usecase import CreateUserUsecase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter


from sqlalchemy.orm import Session


class UserController:
    def __init__(self, db_connection: Session):
        self.user_gateway: IUserRepository = UserRepository(db_connection)
    
    def create_user(self, dto: CreateUserDTO) -> UserDTO:
        create_user_usecase = CreateUserUsecase.build(self.user_gateway)
        user = create_user_usecase.execute(dto)
        return DTOPresenter.transform(user, UserDTO)
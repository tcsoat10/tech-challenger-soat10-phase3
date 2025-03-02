from src.core.ports.user.i_user_repository import IUserRepository
from src.adapters.driven.repositories.user_repository import UserRepository
from src.core.domain.dtos.user.create_user_dto import CreateUserDTO
from src.core.domain.dtos.user.user_dto import UserDTO
from src.application.usecases.user_usecase.create_user_usecase import CreateUserUsecase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.user_usecase.get_user_by_name_usecase import GetUserByNameUsecase
from src.application.usecases.user_usecase.get_user_by_id_usecase import GetUserByIdUsecase
from src.application.usecases.user_usecase.get_all_users_usecase import GetAllUsersUsecase


from sqlalchemy.orm import Session
from typing import Optional, List


class UserController:
    def __init__(self, db_connection: Session):
        self.user_gateway: IUserRepository = UserRepository(db_connection)
    
    def create_user(self, dto: CreateUserDTO) -> UserDTO:
        create_user_usecase = CreateUserUsecase.build(self.user_gateway)
        user = create_user_usecase.execute(dto)
        return DTOPresenter.transform(user, UserDTO)
    
    def get_user_by_name(self, name: str) -> UserDTO:
        user_by_name_usecase = GetUserByNameUsecase.build(self.user_gateway)
        user = user_by_name_usecase.execute(name)
        return DTOPresenter.transform(user, UserDTO)
    
    def get_user_by_id(self, user_id: int) -> UserDTO:
        user_by_id_usecase = GetUserByIdUsecase.build(self.user_gateway)
        user = user_by_id_usecase.execute(user_id)
        return DTOPresenter.transform(user, UserDTO)
    
    def get_all_users(self, include_deleted: Optional[bool]) -> List[UserDTO]:
        all_users_usecase = GetAllUsersUsecase.build(self.user_gateway)
        users = all_users_usecase.execute(include_deleted)
        return DTOPresenter.transform_list(users, UserDTO)
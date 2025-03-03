from sqlalchemy.orm import Session

from src.core.ports.user_profile.i_user_profile_repository import IUserProfileRepository
from src.adapters.driven.repositories.user_profile_repository import UserProfileRepository
from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.adapters.driven.repositories.profile_repository import ProfileRepository
from src.core.ports.user.i_user_repository import IUserRepository
from src.adapters.driven.repositories.user_repository import UserRepository
from src.core.domain.dtos.user_profile.create_user_profile_dto import CreateUserProfileDTO
from src.core.domain.dtos.user_profile.user_profile_dto import UserProfileDTO
from src.application.usecases.user_profile_usecase.create_user_profile_usecase import CreateUserProfileUsecase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter


class UserProfileController:
    def __init__(self, db_connection: Session):
        self.user_profile_gateway: IUserProfileRepository = UserProfileRepository(db_connection)
        self.profile_gateway: IProfileRepository = ProfileRepository(db_connection)
        self.user_gateway: IUserRepository = UserRepository(db_connection)

    def create_user_profile(self, dto: CreateUserProfileDTO) -> UserProfileDTO:
        create_user_profile_usecase = CreateUserProfileUsecase.build(
            self.user_profile_gateway, self.profile_gateway, self.user_gateway
        )
        user_profile = create_user_profile_usecase.execute(dto)
        return DTOPresenter.transform(user_profile, UserProfileDTO)
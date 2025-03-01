from sqlalchemy.orm import Session

from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.adapters.driven.repositories.profile_repository import ProfileRepository
from src.core.domain.dtos.profile.create_profile_dto import CreateProfileDTO
from src.core.domain.dtos.profile.profile_dto import ProfileDTO
from src.application.usecases.profile_usecase.create_profile_usecase import CreateProfileUsecase


class ProfileController:
    def __init__(self, db_connection: Session):
        self.profile_gateway: IProfileRepository = ProfileRepository(db_connection)

    def create_profile(self, dto: CreateProfileDTO) -> ProfileDTO:
        create_profile_usecase = CreateProfileUsecase.build(self.profile_gateway)
        profile = create_profile_usecase.execute(dto)
        return DTOPresenter.transform(profile, ProfileDTO)
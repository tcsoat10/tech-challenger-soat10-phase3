from sqlalchemy.orm import Session

from src.adapters.driven.repositories.permission_repository import PermissionRepository
from src.adapters.driven.repositories.profile_repository import ProfileRepository
from src.core.ports.permission.i_permission_repository import IPermissionRepository
from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.core.domain.dtos.profile_permission.create_profile_permission_dto import CreateProfilePermissionDTO
from src.core.domain.dtos.profile_permission.profile_permission_dto import ProfilePermissionDTO
from src.adapters.driven.repositories.profile_permission_repository import ProfilePermissionRepository
from src.core.ports.profile_permission.i_profile_permission_repository import IProfilePermissionRepository
from src.application.usecases.profile_permission_usecase.create_profile_permission_usecase import CreateProfilePermissionUsecase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter


class ProfilePermissionController:
    def __init__(self, db_connection: Session):
        self.profile_permission_gateway: IProfilePermissionRepository = ProfilePermissionRepository(db_connection)
        self.permission_gateway: IPermissionRepository = PermissionRepository(db_connection)
        self.profile_gateway: IProfileRepository = ProfileRepository(db_connection)
        
    
    def create_profile_permission(self, dto: CreateProfilePermissionDTO) -> ProfilePermissionDTO:
        create_profile_permission_usecase = CreateProfilePermissionUsecase.build(
            self.profile_permission_gateway, self.permission_gateway, self.profile_gateway
        )
        profile_permission = create_profile_permission_usecase.execute(dto)
        return DTOPresenter.transform(profile_permission, ProfilePermissionDTO)

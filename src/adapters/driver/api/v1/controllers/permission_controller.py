from sqlalchemy.orm import Session

from src.core.ports.permission.i_permission_repository import IPermissionRepository
from src.adapters.driven.repositories.permission_repository import PermissionRepository
from src.core.domain.dtos.permission.create_permission_dto import CreatePermissionDTO
from src.core.domain.dtos.permission.permission_dto import PermissionDTO
from src.application.usecases.permission_usecase.create_permission_usecase import CreatePermissionUsecase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.permission_usecase.get_permission_by_name_usecase import GetPermissionByNameUseCase


class PermissionController:
    def __init__(self, db_connection: Session):
        self.permission_gateway: IPermissionRepository = PermissionRepository(db_connection)
    
    def create_permission(self, dto: CreatePermissionDTO) -> PermissionDTO:
        create_permission_usecase = CreatePermissionUsecase.build(self.permission_gateway)
        permission = create_permission_usecase.execute(dto)
        return DTOPresenter.transform(permission, PermissionDTO)
    
    def get_permission_by_name(self, name: str) -> PermissionDTO:
        permission_by_name_usecase = GetPermissionByNameUseCase.build(self.permission_gateway)
        permission = permission_by_name_usecase.execute(name)
        return DTOPresenter.transform(permission, PermissionDTO)
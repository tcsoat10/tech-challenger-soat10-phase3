from sqlalchemy.orm import Session


from src.core.ports.role.i_role_repository import IRoleRepository
from src.adapters.driven.repositories.role_repository import RoleRepository
from src.core.domain.dtos.role.create_role_dto import CreateRoleDTO
from src.core.domain.dtos.role.role_dto import RoleDTO
from src.application.usecases.role_usecase.create_role_usecase import CreateRoleUsecase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.role_usecase.get_role_by_name_usecase import GetRoleByNameUsecase
from src.application.usecases.role_usecase.get_role_by_id_usecase import GetRoleByIdUsecase


class RoleController:
    def __init__(self, db_connection: Session):
        self.role_gateway: IRoleRepository = RoleRepository(db_connection)

    def create_role(self, dto: CreateRoleDTO) -> RoleDTO:
        create_role_usecase = CreateRoleUsecase.build(self.role_gateway)
        role = create_role_usecase.execute(dto)
        return DTOPresenter.transform(role, RoleDTO)
    
    def get_role_by_name(self, name: str) -> RoleDTO:
        role_by_name_usecase = GetRoleByNameUsecase.build(self.role_gateway)
        role = role_by_name_usecase.exexute(name)
        return DTOPresenter.transform(role, RoleDTO)
    
    def get_role_by_id(self, role_id: int) -> RoleDTO:
        role_by_id_usecase = GetRoleByIdUsecase.build(self.role_gateway)
        role = role_by_id_usecase.exexute(role_id)
        return DTOPresenter.transform(role, RoleDTO)
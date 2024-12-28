from src.core.ports.permission.i_permission_repository import IPermissionRepository


class PermissionService(IPermissionRepository):
    def __init__(self, repository: IPermissionRepository):
        self.repository = repository

    def create_permission(self, dto)
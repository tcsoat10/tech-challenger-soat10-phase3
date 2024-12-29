from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db
from src.core.ports.permission.i_permission_service import IPermissionService
from src.core.ports.permission.i_permission_repository import IPermissionRepository
from src.adapters.driven.repositories.permission_repository import PermissionRepository
from src.application.services.permission_service import PermissionService
from src.core.domain.dtos.permission.permission_dto import PermissionDTO
from src.core.domain.dtos.permission.create_permission_dto import CreatePermissionDTO


router = APIRouter()


def _get_permission_service(db_session: Session = Depends(get_db)) -> IPermissionService:
    repository: IPermissionRepository = PermissionRepository(db_session)
    return PermissionService(repository)


@router.post(path='/permissions', response_model=PermissionDTO, status_code=status.HTTP_201_CREATED)
def create_permission(dto: CreatePermissionDTO, service: IPermissionService = Depends(_get_permission_service)) -> PermissionDTO:
    return service.create_permission(dto)

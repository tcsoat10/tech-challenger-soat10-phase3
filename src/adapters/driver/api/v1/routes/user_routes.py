from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from config.database import get_db
from src.core.ports.user.i_user_service import IUserService
from src.core.ports.user.i_user_repository import IUserRepository
from src.adapters.driven.repositories.user_repository import UserRepository
from src.core.domain.dtos.user.user_dto import UserDTO
from src.core.domain.dtos.user.create_user_dto import CreateUserDTO
from src.application.services.user_service import UserService
from src.core.domain.dtos.user.update_user_dto import UpdateUserDTO


router = APIRouter()


def _get_user_service(db_session: Session = Depends(get_db)) -> IUserService:
    repository: IUserRepository = UserRepository(db_session)
    return UserService(repository)


@router.post(path='/users', response_model=UserDTO, status_code=status.HTTP_201_CREATED)
def create_user(dto: CreateUserDTO, service: IUserService = Depends(_get_user_service)):
    return service.create_user(dto)


@router.get(path='/users/{user_name}/name', response_model=UserDTO, status_code=status.HTTP_200_OK)
def get_user_by_name(user_name: str, service: IUserService = Depends(_get_user_service)):
    return service.get_user_by_name(user_name)


@router.get(path='/users/{user_id}/id', response_model=UserDTO, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int, service: IUserService = Depends(_get_user_service)):
    return service.get_user_by_id(user_id)


@router.get(path='/users', response_model=List[UserDTO], status_code=status.HTTP_200_OK)
def get_all_users(service: IUserService = Depends(_get_user_service)):
    return service.get_all_users()


@router.put(path='/users/{user_id}', response_model=UserDTO, status_code=status.HTTP_200_OK)
def update_user(user_id: int, dto: UpdateUserDTO, service: IUserService = Depends(_get_user_service)):
    return service.update_user(user_id, dto)


@router.delete(path='/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, service: IUserService = Depends(_get_user_service)):
    service.delete_user(user_id)
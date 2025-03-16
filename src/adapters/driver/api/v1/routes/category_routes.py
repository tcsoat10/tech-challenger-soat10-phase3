from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query, Security
from dependency_injector.wiring import inject, Provide

from src.adapters.driver.api.v1.controllers.category_controller import CategoryController
from src.core.auth.dependencies import get_current_user
from src.constants.permissions import CategoryPermissions
from src.core.domain.dtos.category.update_category_dto import UpdateCategoryDTO
from src.adapters.driven.repositories.category_repository import CategoryRepository
from src.core.domain.dtos.category.category_dto import CategoryDTO
from src.core.domain.dtos.category.create_category_dto import CreateCategoryDTO
from src.core.containers import Container

router = APIRouter()

@router.post(
    "/categories",
    response_model=CategoryDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=[CategoryPermissions.CAN_CREATE_CATEGORY])]
)
@inject
def create_category(
    dto: CreateCategoryDTO,
    controller: CategoryController = Depends(Provide[Container.category_controller]),
    user: dict = Security(get_current_user)
):
    return controller.create_category(dto)

@router.get(
    "/categories/{category_name}/name",
    response_model=CategoryDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[CategoryPermissions.CAN_VIEW_CATEGORIES])]
)
@inject
def get_category_by_name(
    category_name: str,
    controller: CategoryController = Depends(Provide[Container.category_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_category_by_name(name=category_name)

@router.get(
    "/categories/{category_id}/id",
    response_model=CategoryDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[CategoryPermissions.CAN_VIEW_CATEGORIES])]
)
@inject
def get_category_by_id(
    category_id: int,
    controller: CategoryRepository = Depends(Provide[Container.category_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_category_by_id(category_id=category_id)

@router.get(
    "/categories",
    response_model=List[CategoryDTO],
    dependencies=[Security(get_current_user, scopes=[CategoryPermissions.CAN_VIEW_CATEGORIES])]
)
@inject
def get_all_categories(
    include_deleted: Optional[bool] = Query(False),
    controller: CategoryController = Depends(Provide[Container.category_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_all_categories(include_deleted=include_deleted)

@router.put(
    "/categories/{category_id}",
    response_model=CategoryDTO,
    dependencies=[Security(get_current_user, scopes=[CategoryPermissions.CAN_UPDATE_CATEGORY])]
)
@inject
def update_category(
    category_id: int,
    dto: UpdateCategoryDTO,
    controller: CategoryController = Depends(Provide[Container.category_controller]),
    user: dict = Security(get_current_user)
):
    return controller.update_category(category_id, dto)

@router.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=[CategoryPermissions.CAN_DELETE_CATEGORY])]
)
@inject
def delete_category(
    category_id: int,
    controller: CategoryController = Depends(Provide[Container.category_controller]),
    user: dict = Security(get_current_user)
):
    controller.delete_category(category_id)

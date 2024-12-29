from typing import List, Optional
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from config.database import get_db
from src.core.domain.dtos.category.update_category_dto import UpdateCategoryDTO
from src.adapters.driven.repositories.category_repository import CategoryRepository
from src.application.services.category_service import CategoryService
from src.core.domain.dtos.category.category_dto import CategoryDTO
from src.core.domain.dtos.category.create_category_dto import CreateCategoryDTO
from src.core.ports.category.i_category_repository import ICategoryRepository
from src.core.ports.category.i_category_service import ICategoryService

router = APIRouter()

# Substituir por lib DI.
def _get_category_service(db_session: Session = Depends(get_db)) -> ICategoryService:
    repository: ICategoryRepository = CategoryRepository(db_session)
    return CategoryService(repository)

@router.post("/categories", response_model=CategoryDTO, status_code=status.HTTP_201_CREATED)
def create_category(dto: CreateCategoryDTO, service: ICategoryService = Depends(_get_category_service)):
    return service.create_category(dto)

@router.get("/categories/{category_name}/name", response_model=CategoryDTO, status_code=status.HTTP_200_OK)
def get_category_by_name(category_name: str, service: ICategoryService = Depends(_get_category_service)):
    return service.get_category_by_name(name=category_name)

@router.get("/categories/{category_id}/id", response_model=CategoryDTO, status_code=status.HTTP_200_OK)
def get_category_by_id(category_id: int, service: ICategoryService = Depends(_get_category_service)):
    return service.get_category_by_id(category_id=category_id)

@router.get("/categories", response_model=List[CategoryDTO])
def get_all_categories(include_deleted: Optional[bool] = Query(False), service: ICategoryService = Depends(_get_category_service)):
    return service.get_all_categories(include_deleted=include_deleted)

@router.put("/categories/{category_id}", response_model=CategoryDTO)
def update_category(category_id: int, dto: UpdateCategoryDTO, service: ICategoryService = Depends(_get_category_service)):
    return service.update_category(category_id, dto)

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, service: ICategoryService = Depends(_get_category_service)):
    service.delete_category(category_id)

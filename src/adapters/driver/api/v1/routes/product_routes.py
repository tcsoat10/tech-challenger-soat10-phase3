from typing import Optional
from fastapi import APIRouter, Depends, Query, Security, status
from sqlalchemy.orm import Session

from src.adapters.driver.api.v1.controllers.product_controller import ProductController
from config.database import get_db
from src.constants.permissions import ProductPermissions
from src.core.auth.dependencies import get_current_user
from src.core.domain.dtos.product.update_product_dto import UpdateProductDTO
from src.adapters.driven.repositories.category_repository import CategoryRepository
from src.core.ports.category.i_category_repository import ICategoryRepository
from src.adapters.driven.repositories.product_repository import ProductRepository
from src.application.services.product_service import ProductService
from src.core.domain.dtos.product.create_product_dto import CreateProductDTO
from src.core.domain.dtos.product.product_dto import ProductDTO
from src.core.ports.product.i_product_repository import IProductRepository
from src.core.ports.product.i_product_service import IProductService

router = APIRouter()

# Substituir por lib DI.
def _get_product_service(db_session: Session = Depends(get_db)) -> IProductService:
    product_repository: IProductRepository = ProductRepository(db_session)
    category_repository: ICategoryRepository = CategoryRepository(db_session)
    return ProductService(product_repository, category_repository)

def _get_product_controller(db_session: Session = Depends(get_db)):
    return ProductController(db_session)

@router.post(
    "/products",
    response_model=ProductDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=[ProductPermissions.CAN_CREATE_PRODUCT])]
)
def create_product(
    dto: CreateProductDTO,
    controller: ProductController = Depends(_get_product_controller),
    user=Depends(get_current_user)
):
    return controller.create_product(dto)

@router.get(
    "/products/{product_name}/name",
    response_model=ProductDTO, status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[ProductPermissions.CAN_VIEW_PRODUCTS])]
)
def get_product_by_name(
    product_name: str,
    controller: ProductController = Depends(_get_product_controller),
    user=Depends(get_current_user)
):
    return controller.get_product_by_name(name=product_name)

@router.get(
    "/products/{product_id}/id",
    response_model=ProductDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[ProductPermissions.CAN_VIEW_PRODUCTS])]
)
def get_product_by_id(
    product_id: int,
    controller: ProductController = Depends(_get_product_controller),
    user=Depends(get_current_user)
):
    return controller.get_product_by_id(product_id=product_id)

@router.get(
    "/products",
    response_model=list[ProductDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[ProductPermissions.CAN_VIEW_PRODUCTS])]
)
def get_all_products(
    include_deleted: Optional[bool] = Query(False),
    categories: Optional[list[str]] = Query(None),
    controller: ProductController = Depends(_get_product_controller),
    user=Depends(get_current_user)
):
    return controller.get_all_products(categories=categories, include_deleted=include_deleted)

@router.put(
    "/products/{product_id}",
    response_model=ProductDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[ProductPermissions.CAN_UPDATE_PRODUCT])]
)
def update_product(
    product_id: int,
    dto: UpdateProductDTO,
    controller: ProductController = Depends(_get_product_controller),
    user=Depends(get_current_user)
):
    return controller.update_product(product_id, dto)

@router.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=[ProductPermissions.CAN_DELETE_PRODUCT])]
)
def delete_product(product_id: int, service: IProductService = Depends(_get_product_service)):
    service.delete_product(product_id)

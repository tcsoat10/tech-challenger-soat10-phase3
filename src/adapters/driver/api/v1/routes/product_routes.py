from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db
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

@router.post("/products", response_model=ProductDTO, status_code=status.HTTP_201_CREATED)
def create_product(dto: CreateProductDTO, service: IProductService = Depends(_get_product_service)):
    return service.create_product(dto)


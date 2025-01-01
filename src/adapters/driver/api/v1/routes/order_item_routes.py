from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.adapters.driven.repositories.order_item_repository import OrderItemRepository
from src.adapters.driven.repositories.product_repository import ProductRepository
from src.application.services.order_item_service import OrderItemService
from config.database import get_db
from src.core.domain.dtos.order_item.create_order_item_dto import CreateOrderItemDTO
from src.core.domain.dtos.order_item.order_item_dto import OrderItemDTO
from src.core.domain.dtos.order_item.update_order_item_dto import UpdateOrderItemDTO
from src.core.ports.order_item.i_order_item_repository import IOrderItemRepository
from src.core.ports.order_item.i_order_item_service import IOrderItemService
from src.core.ports.product.i_product_repository import IProductRepository


router = APIRouter()

# Substituir por lib DI.
def _get_order_item_service(db_session: Session = Depends(get_db)) -> IOrderItemService:
    order_item_repository: IOrderItemRepository = OrderItemRepository(db_session)
    product_repository: IProductRepository = ProductRepository(db_session)
    return OrderItemService(order_item_repository, product_repository)

@router.post("/order-items", response_model=OrderItemDTO, status_code=status.HTTP_201_CREATED)
def create_order_item(dto: CreateOrderItemDTO, service: IOrderItemService = Depends(_get_order_item_service)):
    return service.create_order_item(dto)

@router.get("/order-items/{order_item_id}/id", response_model=OrderItemDTO, status_code=status.HTTP_200_OK)
def get_order_item_by_id(order_item_id: int, service: IOrderItemService = Depends(_get_order_item_service)):
    return service.get_order_item_by_id(order_item_id)

@router.get("/order-items", response_model=list[OrderItemDTO])
def get_all_order_items(include_deleted: bool = False, service: IOrderItemService = Depends(_get_order_item_service)):
    return service.get_all_order_items(include_deleted)

@router.put("/order-items/{order_item_id}", response_model=OrderItemDTO)
def update_order_item(order_item_id: int, dto: UpdateOrderItemDTO, service: IOrderItemService = Depends(_get_order_item_service)):
    return service.update_order_item(order_item_id, dto)

@router.delete("/order-items/{order_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_item(order_item_id: int, service: IOrderItemService = Depends(_get_order_item_service)):
    service.delete_order_item(order_item_id)

from fastapi import APIRouter, Depends, status, Security
from sqlalchemy.orm import Session
from dependency_injector.wiring import inject, Provide

from src.adapters.driver.api.v1.controllers.order_item_controller import OrderItemController
from src.adapters.driven.repositories.order_repository import OrderRepository
from src.core.ports.order.i_order_repository import IOrderRepository
from src.adapters.driven.repositories.order_item_repository import OrderItemRepository
from src.adapters.driven.repositories.product_repository import ProductRepository
from config.database import get_db
from src.core.domain.dtos.order_item.create_order_item_dto import CreateOrderItemDTO
from src.core.domain.dtos.order_item.order_item_dto import OrderItemDTO
from src.core.domain.dtos.order_item.update_order_item_dto import UpdateOrderItemDTO
from src.core.ports.order_item.i_order_item_repository import IOrderItemRepository
from src.core.ports.product.i_product_repository import IProductRepository
from src.core.auth.dependencies import get_current_user
from src.constants.permissions import OrderItemPermissions
from src.core.containers import Container


router = APIRouter()

def _get_order_item_controller(db_session: Session = Depends(get_db)):
    order_gateway: IOrderRepository = OrderRepository(db_session)
    product_gateway: IProductRepository = ProductRepository(db_session)
    order_item_gateway: IOrderItemRepository = OrderItemRepository(db_session)
    return OrderItemController(order_item_gateway, product_gateway, order_gateway)

@router.post(
        "/order-items",
        response_model=OrderItemDTO,
        status_code=status.HTTP_201_CREATED,
        dependencies=[Security(get_current_user, scopes=[OrderItemPermissions.CAN_CREATE_ORDER_ITEM])]
)
@inject
def create_order_item(
    dto: CreateOrderItemDTO,
    controller: OrderItemController = Depends(Provide[Container.order_item_controller]),
    user: dict = Security(get_current_user)
):
    return controller.create_order_item(dto)

@router.get(
        "/order-items/{order_item_id}/id",
        response_model=OrderItemDTO,
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[OrderItemPermissions.CAN_VIEW_ORDER_ITEMS])]
)
@inject
def get_order_item_by_id(
    order_item_id: int,
    controller: OrderItemController = Depends(Provide[Container.order_item_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_order_item_by_id(order_item_id)

@router.get(
        "/order-items",
        response_model=list[OrderItemDTO],
        dependencies=[Security(get_current_user, scopes=[OrderItemPermissions.CAN_VIEW_ORDER_ITEMS])]
)
@inject
def get_all_order_items(
    include_deleted: bool = False,
    controller: OrderItemController = Depends(Provide[Container.order_item_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_all_order_items(include_deleted)

@router.put(
        "/order-items/{order_item_id}",
        response_model=OrderItemDTO,
        dependencies=[Security(get_current_user, scopes=[OrderItemPermissions.CAN_UPDATE_ORDER_ITEM])]
)
@inject
def update_order_item(
    order_item_id: int,
    dto: UpdateOrderItemDTO,
    controller: OrderItemController = Depends(Provide[Container.order_item_controller]),
    user: dict = Security(get_current_user)
):
    return controller.update_order_item(order_item_id, dto)

@router.delete(
        "/order-items/{order_item_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        dependencies=[Security(get_current_user, scopes=[OrderItemPermissions.CAN_DELETE_ORDER_ITEM])]
)
@inject
def delete_order_item(
    order_item_id: int,
    controller: OrderItemController = Depends(Provide[Container.order_item_controller]),
    user: dict = Security(get_current_user)
):
    controller.delete_order_item(order_item_id)

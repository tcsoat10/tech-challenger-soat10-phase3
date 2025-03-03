from typing import List, Optional
from fastapi import APIRouter, Depends, status, Security, Query
from sqlalchemy.orm import Session

from config.database import get_db
from src.adapters.driver.api.v1.controllers.order_status_controller import OrderStatusController
from src.core.domain.dtos.order_status.update_order_status_dto import UpdateOrderStatusDTO
from src.adapters.driven.repositories.order_status_repository import OrderStatusRepository
from src.application.services.order_status_service import OrderStatusService
from src.core.domain.dtos.order_status.order_status_dto import OrderStatusDTO
from src.core.domain.dtos.order_status.create_order_status_dto import CreateOrderStatusDTO
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.core.ports.order_status.i_order_status_service import IOrderStatusService
from src.core.auth.dependencies import get_current_user
from src.constants.permissions import OrderStatusPermissions

router = APIRouter()

# Substituir por lib DI.
def _get_order_status_service(db_session: Session = Depends(get_db)) -> IOrderStatusService:
    repository: IOrderStatusRepository = OrderStatusRepository(db_session)
    return OrderStatusService(repository)

def _get_order_status_controller(db_session: Session = Depends(get_db)) -> OrderStatusController:
    return OrderStatusController(db_session)

@router.post(
        "/order_status",
        response_model=OrderStatusDTO,
        status_code=status.HTTP_201_CREATED,
        dependencies=[Security(get_current_user, scopes=[OrderStatusPermissions.CAN_CREATE_ORDER_STATUS])]
)
def create_order_status(
    dto: CreateOrderStatusDTO,
    controller: OrderStatusController = Depends(_get_order_status_controller),
    user: dict = Security(get_current_user)
):
    return controller.create_order_status(dto)

@router.get(
        "/order_status/{order_status}/status",
        response_model=OrderStatusDTO,
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[OrderStatusPermissions.CAN_VIEW_ORDER_STATUSES])]
)
def get_order_status_by_status(
    order_status: str,
    controller: OrderStatusController = Depends(_get_order_status_controller),
    user: dict = Security(get_current_user)
):
    return controller.get_order_status_by_status(status=order_status)

@router.get(
        "/order_status/{order_status_id}/id",
        response_model=OrderStatusDTO,
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[OrderStatusPermissions.CAN_VIEW_ORDER_STATUSES])]
)
def get_order_status_by_id(
    order_status_id: int,
    controller: OrderStatusController = Depends(_get_order_status_controller),
    user: dict = Security(get_current_user)
):
    return controller.get_order_status_by_id(order_status_id=order_status_id)

@router.get(
        "/order_status",
        response_model=List[OrderStatusDTO],
        dependencies=[Security(get_current_user, scopes=[OrderStatusPermissions.CAN_VIEW_ORDER_STATUSES])]
)
def get_all_order_status(
    include_deleted: Optional[bool] = Query(False),
    controller: OrderStatusController = Depends(_get_order_status_controller),
    user: dict = Security(get_current_user)
):
    return controller.get_all_orders_status(include_deleted=include_deleted)

@router.put(
        "/order_status/{order_status_id}",
        response_model=OrderStatusDTO,
        dependencies=[Security(get_current_user, scopes=[OrderStatusPermissions.CAN_UPDATE_ORDER_STATUS])]
)
def update_order_status(
    order_status_id: int,
    dto: UpdateOrderStatusDTO,
    service: IOrderStatusService = Depends(_get_order_status_service),
    user: dict = Security(get_current_user)
):
    return service.update_order_status(order_status_id, dto)

@router.delete(
        "/order_status/{order_status_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        dependencies=[Security(get_current_user, scopes=[OrderStatusPermissions.CAN_DELETE_ORDER_STATUS])]
)
def delete_order_status(
    order_status_id: int,
    service: IOrderStatusService = Depends(_get_order_status_service),
    user: dict = Security(get_current_user)
):
    service.delete_order_status(order_status_id)

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db
from src.core.domain.dtos.order_status.update_order_status_dto import UpdateOrderStatusDTO
from src.adapters.driven.repositories.order_status_repository import OrderStatusRepository
from src.application.services.order_status_service import OrderStatusService
from src.core.domain.dtos.order_status.order_status_dto import OrderStatusDTO
from src.core.domain.dtos.order_status.create_order_status_dto import CreateOrderStatusDTO
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.core.ports.order_status.i_order_status_service import IOrderStatusService

router = APIRouter()

# Substituir por lib DI.
def _get_order_status_service(db_session: Session = Depends(get_db)) -> IOrderStatusService:
    repository: IOrderStatusRepository = OrderStatusRepository(db_session)
    return OrderStatusService(repository)

@router.post("/order_status", response_model=OrderStatusDTO, status_code=status.HTTP_201_CREATED)
def create_order_status(dto: CreateOrderStatusDTO, service: IOrderStatusService = Depends(_get_order_status_service)):
    return service.create_order_status(dto)

@router.get("/order_status/{order_status}/status", response_model=OrderStatusDTO, status_code=status.HTTP_200_OK)
def get_order_status_by_status(order_status: str, service: IOrderStatusService = Depends(_get_order_status_service)):
    return service.get_order_status_by_status(status=order_status)

@router.get("/order_status/{order_status_id}/id", response_model=OrderStatusDTO, status_code=status.HTTP_200_OK)
def get_order_status_by_id(order_status_id: int, service: IOrderStatusService = Depends(_get_order_status_service)):
    return service.get_order_status_by_id(order_status_id=order_status_id)

@router.get("/order_status", response_model=List[OrderStatusDTO])
def get_all_order_status(service: IOrderStatusService = Depends(_get_order_status_service)):
    return service.get_all_orders_status()

@router.put("/order_status/{order_status_id}", response_model=OrderStatusDTO)
def update_order_status(order_status_id: int, dto: UpdateOrderStatusDTO, service: IOrderStatusService = Depends(_get_order_status_service)):
    return service.update_order_status(order_status_id, dto)

@router.delete("/order_status/{order_status_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_status(order_status_id: int, service: IOrderStatusService = Depends(_get_order_status_service)):
    service.delete_order_status(order_status_id)

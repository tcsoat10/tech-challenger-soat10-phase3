from typing import List, Optional
from config.database import DELETE_MODE
from src.core.domain.dtos.order_status.update_order_status_dto import UpdateOrderStatusDTO
from src.core.domain.dtos.order_status.create_order_status_dto import CreateOrderStatusDTO
from src.core.domain.dtos.order_status.order_status_dto import OrderStatusDTO
from src.core.domain.entities.order_status import OrderStatus
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.core.ports.order_status.i_order_status_service import IOrderStatusService


class OrderStatusService(IOrderStatusService):

    def __init__(self, repository: IOrderStatusRepository):
        self.repository = repository
            
    def create_order_status(self, dto: CreateOrderStatusDTO) -> OrderStatusDTO:
        if self.repository.exists_by_status(dto.status):
            raise EntityDuplicatedException(entity_name="OrderStatus")
        
        order_status = OrderStatus(
            status=dto.status,
            description=dto.description
        )

        order_status = self.repository.create(order_status)
        return OrderStatusDTO.from_entity(order_status)
    
    def get_order_status_by_status(self, status: str) -> OrderStatusDTO:
        order_status = self.repository.get_by_status(status=status)
        if not order_status:
            raise EntityNotFoundException(entity_name="OrderStatus")
        return OrderStatusDTO.from_entity(order_status)

    def get_order_status_by_id(self, order_status_id: int) -> OrderStatusDTO:
        order_status = self.repository.get_by_id(order_status_id=order_status_id)
        if not order_status:
            raise EntityNotFoundException(entity_name="OrderStatus")
        return OrderStatusDTO.from_entity(order_status)

    def get_all_orders_status(self, include_deleted: Optional[bool] = False) -> List[OrderStatusDTO]:
        order_status = self.repository.get_all(include_deleted=include_deleted)
        return [OrderStatusDTO.from_entity(order_status) for order_status in order_status]

    def update_order_status(self, order_status_id: int, dto: UpdateOrderStatusDTO) -> OrderStatusDTO:
        order_status = self.repository.get_by_id(order_status_id)
        if not order_status:
            raise EntityDuplicatedException(entity_name="OrderStatus")
    
        order_status.status=dto.status,
        order_status.description=dto.description
        
        order_status = self.repository.update(order_status)

        return OrderStatusDTO.from_entity(order_status)

    def delete_order_status(self, order_status_id: int) -> None:
        order_status = self.repository.get_by_id(order_status_id)
        if not order_status:
            raise EntityNotFoundException(entity_name="OrderStatus")
        
        if DELETE_MODE == 'soft':
            if order_status.is_deleted():
                raise EntityNotFoundException(entity_name="OrderStatus")

            order_status.soft_delete()
            self.repository.update(order_status)
        else:
            self.repository.delete(order_status)

__all__ = ["OrderStatusService"]

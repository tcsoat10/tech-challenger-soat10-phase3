from config.database import DELETE_MODE
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.domain.dtos.order_item.order_item_dto import OrderItemDTO
from src.core.domain.dtos.order_item.update_order_item_dto import UpdateOrderItemDTO
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.order_item.i_order_item_repository import IOrderItemRepository
from src.core.ports.order_item.i_order_item_service import IOrderItemService
from src.core.ports.product.i_product_repository import IProductRepository


class OrderItemService(IOrderItemService):

    def __init__(self, repository: IOrderItemRepository, product_repository: IProductRepository, order_repository: IOrderRepository):
        self.repository = repository
        self.product_repository = product_repository
        self.order_repository = order_repository

    
    def delete_order_item(self, order_item_id: int) -> None:
        order_item = self.repository.get_by_id(order_item_id)
        if not order_item:
            raise EntityNotFoundException(entity_name="Order Item")
        
        if DELETE_MODE == 'soft':
            if order_item.is_deleted():
                raise EntityNotFoundException(entity_name="Order Item")

            order_item.soft_delete()
            self.repository.update(order_item)
        else:
            self.repository.delete(order_item)

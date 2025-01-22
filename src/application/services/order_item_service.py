from typing import List
from config.database import DELETE_MODE
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.domain.dtos.order_item.create_order_item_dto import CreateOrderItemDTO
from src.core.domain.dtos.order_item.order_item_dto import OrderItemDTO
from src.core.domain.dtos.order_item.update_order_item_dto import UpdateOrderItemDTO
from src.core.domain.entities.order_item import OrderItem
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.order_item.i_order_item_repository import IOrderItemRepository
from src.core.ports.order_item.i_order_item_service import IOrderItemService
from src.core.ports.product.i_product_repository import IProductRepository


class OrderItemService(IOrderItemService):

    def __init__(self, repository: IOrderItemRepository, product_repository: IProductRepository, order_repository: IOrderRepository):
        self.repository = repository
        self.product_repository = product_repository
        self.order_repository = order_repository

    def create_order_item(self, dto: CreateOrderItemDTO) -> OrderItemDTO:
        product = self.product_repository.get_by_id(dto.product_id)
        if not product:
            raise EntityNotFoundException(entity_name="Product")

        if not dto.order_id:
            raise EntityNotFoundException(entity_name="Order ID")

        order = self.order_repository.get_by_id(dto.order_id)
        if not order:
            raise EntityNotFoundException(entity_name="Order")

        order_item = OrderItem(
            order=order,
            product=product,
            quantity=dto.quantity,
            observation=dto.observation,
        )

        order_item = self.repository.create(order_item)
        return OrderItemDTO.from_entity(order_item)
    
    def get_order_item_by_order_id(self, order_id: int, include_deleted: bool = False) -> List[OrderItemDTO]:
        order_items = self.repository.get_by_order_id(order_id, include_deleted)
        return [OrderItemDTO.from_entity(order_item) for order_item in order_items]

    def get_order_item_by_product_name(self, order_id: int, product_name: str) -> OrderItemDTO:
        order_item = self.repository.get_by_product_name(order_id, product_name)
        return OrderItemDTO.from_entity(order_item)
    
    def get_order_item_by_id(self, order_item_id: int) -> OrderItemDTO:
        order_item = self.repository.get_by_id(order_item_id)
        if not order_item:
            raise EntityNotFoundException(entity_name="Order Item")
        return OrderItemDTO.from_entity(order_item)
    
    def get_all_order_items(self, include_deleted: bool = False) -> List[OrderItemDTO]:
        order_items = self.repository.get_all(include_deleted)
        return [OrderItemDTO.from_entity(order_item) for order_item in order_items]
    
    def update_order_item(self, order_item_id: int, dto: UpdateOrderItemDTO) -> OrderItemDTO:
        order_item = self.repository.get_by_id(order_item_id)
        if not order_item:
            raise EntityNotFoundException(entity_name="Order Item")

        product = self.product_repository.get_by_id(dto.product_id)
        if not product:
            raise EntityNotFoundException(entity_name="Product")

        order_item.product = product
        order_item.quantity = dto.quantity
        order_item.observation = dto.observation

        order_item = self.repository.update(order_item)
        return OrderItemDTO.from_entity(order_item)
    
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

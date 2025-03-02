from typing import List, Optional
from src.core.ports.product.i_product_repository import IProductRepository
from src.constants.order_status import OrderStatusEnum
from src.core.domain.entities.order_item import OrderItem
from src.core.exceptions.bad_request_exception import BadRequestException
from src.core.ports.employee.i_employee_repository import IEmployeeRepository
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.domain.dtos.order.order_dto import OrderDTO
from src.core.domain.entities.order import Order
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.order.i_order_service import IOrderService


class OrderService(IOrderService):

    def __init__(
        self,
        repository: IOrderRepository,
        order_status_repository: IOrderStatusRepository,
        customer_repository: ICustomerRepository,
        employee_repository:IEmployeeRepository,
        product_repository: IProductRepository,
    ):
        self.order_repository = repository
        self.order_status_repository = order_status_repository
        self.customer_repository = customer_repository
        self.employee_repository = employee_repository
        self.product_repository = product_repository

    def go_back(self, order_id: int, current_user: dict) -> None:
        order = self._get_order(order_id, current_user)
        order.revert_order_status(self.order_status_repository)
        self.order_repository.update(order)

    def _get_order(self, order_id: int, current_user: dict) -> Order:
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise EntityNotFoundException(message=f"O pedido com ID '{order_id}' não foi encontrado.")

        if current_user['profile']['name'] in ['customer', 'anonymous'] and order.id_customer != int(current_user['person']['id']):
            raise EntityNotFoundException(message=f"O pedido com ID '{order_id}' não foi encontrado.")
        
        return order

    def _get_item_from_order(self, order: Order, item_id: int) -> OrderItem:
        order_item = next((order_item for order_item in order.order_items if order_item.id == item_id), None)
        if not order_item:
            raise EntityNotFoundException(message=f"O item com ID '{item_id}' não foi encontrado no pedido.")
        return order_item

__all__ = ["OrderService"]

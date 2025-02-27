from typing import List, Optional
from src.core.ports.product.i_product_repository import IProductRepository
from src.constants.order_status import OrderStatusEnum
from src.core.domain.dtos.order_item.order_item_dto import OrderItemDTO
from src.core.domain.entities.order_item import OrderItem
from src.core.exceptions.bad_request_exception import BadRequestException
from src.core.domain.dtos.order_item.create_order_item_dto import CreateOrderItemDTO
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

    def next_step(self, order_id: int, current_user: dict) -> None:
        order = self._get_order(order_id, current_user)

        if order.order_status.status in [
            OrderStatusEnum.ORDER_PAID.status,
            OrderStatusEnum.ORDER_PREPARING.status,
            OrderStatusEnum.ORDER_READY.status,
        ] and current_user['profile']['name'] not in ['employee', 'manager']:
            raise BadRequestException("Você não tem permissão para avançar o pedido para o próximo passo.")

        if order.order_status.status in [
            OrderStatusEnum.ORDER_PENDING.status,
            OrderStatusEnum.ORDER_WAITING_BURGERS.status,
            OrderStatusEnum.ORDER_WAITING_SIDES.status,
            OrderStatusEnum.ORDER_WAITING_DRINKS.status,
            OrderStatusEnum.ORDER_WAITING_DESSERTS.status,
            OrderStatusEnum.ORDER_READY_TO_PLACE.status,
            OrderStatusEnum.ORDER_PLACED.status,
        ] and current_user['profile']['name'] not in ['customer', 'anonymous']:
            raise BadRequestException("Você não tem permissão para avançar o pedido para o próximo passo.")

        employee_id = int(current_user['person']['id']) if current_user['profile']['name'] in ['employee', 'manager'] else None
        employee = self.employee_repository.get_by_id(employee_id)
        order.next_step(self.order_status_repository, employee=employee)
        order = self.order_repository.update(order)

        return {"detail": f"Pedido avançado para o próximo passo: {order.order_status.status}"}

    def go_back(self, order_id: int, current_user: dict) -> None:
        order = self._get_order(order_id, current_user)
        order.go_back(self.order_status_repository)
        self.order_repository.update(order)

    def list_orders(self, current_user: dict, status: Optional[List[str]] = None) -> List[OrderDTO]:
        if current_user['profile']['name'] == 'customer':
            customer_id = int(current_user['person']['id'])
            orders = self.order_repository.get_all(status=status, customer_id=customer_id)
        else:
            orders = self.order_repository.get_all(status=status)

        return [OrderDTO.from_entity(order) for order in orders]

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
